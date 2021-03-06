# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game


#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='OffensivePlanningAgent', second='DefensiveReflexAgent'):
    """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

    # The following line is an example only; feel free to change it.
    return [eval(first)(firstIndex), eval(second)(secondIndex)]


##########
# Agents #
##########

class OffensivePlanningAgent(CaptureAgent):
    def registerInitialState(self, gameState):
        self.start = gameState.getAgentPosition(self.index)
        CaptureAgent.registerInitialState(self, gameState)

        # ????????? ??? ????????? ????????? ?????? X ?????? ??????
        self.boundaryX = (gameState.data.layout.width - 2) // 2

        if not self.red:
            self.boundaryX += 1

        # ????????? ??? ????????? ????????? ?????? ?????? ?????? ??????
        self.boundaries = []
        for i in range(gameState.data.layout.height):
            if not gameState.hasWall(self.boundaryX, i):
                self.boundaries.append((self.boundaryX, i))

    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)
        self.debugClear()

        if gameState.getAgentState(self.index).numCarrying == 0:
            values = [self.depthLimitedSearchToFood(gameState, action, 1) for action in actions if action != Directions.STOP]
        else:
            values = [self.depthLimitedSearchToHome(gameState, action, 1) for action in actions if action != Directions.STOP]

        # ?????? ??? ????????? ?????? ????????? ????????? ???????????? ??????
        maxValue = max(values)
        bestActions = [action for action, value in zip(actions, values) if value == maxValue]

        return random.choice(bestActions)

    def depthLimitedSearchToFood(self, gameState, action, depth):
        successor = self.getSuccessor(gameState, action)
        agentState = successor.getAgentState(self.index)
        pos = agentState.getPosition()

        foodList = self.getFood(successor).asList()

        if depth >= 4:
            return -min([self.getMazeDistance(pos, food) for food in foodList])

        if pos == self.start:
            return -9999

        if agentState.isPacman:
            enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
            # scared timer??? 0??? ghost??? ????????? ????????? ?????? ??? ?????? enemy??? ????????? enemyDistance??? inf??? ????????? search??? ?????? ??????
            enemyDistance = min([self.getMazeDistance(agentState.getPosition(), enemy.getPosition()) for enemy in enemies if enemy.scaredTimer == 0], default=9999)

            if enemyDistance <= depth or pos == self.start:
                return -9999

        if agentState.numCarrying > 0:
            return 100

        actions = successor.getLegalActions(self.index)
        return 0.9 * max([self.depthLimitedSearchToFood(successor, action, depth + 1) for action in actions])

    def depthLimitedSearchToHome(self, gameState, action, depth):
        successor = self.getSuccessor(gameState, action)
        agentState = successor.getAgentState(self.index)
        pos = agentState.getPosition()

        if depth >= 4:
            return -min([self.getMazeDistance(pos, boundary) for boundary in self.boundaries])

        if self.getScore(successor) - self.getScore(gameState) > 0:
            return 100

        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        # scared timer??? 0??? ghost??? ????????? ????????? ?????? ??? ?????? enemy??? ????????? enemyDistance??? inf??? ????????? search??? ?????? ??????
        enemyDistance = min([self.getMazeDistance(agentState.getPosition(), enemy.getPosition()) for enemy in enemies if enemy.scaredTimer == 0], default=9999)

        if enemyDistance <= depth or pos == self.start:
            return -9999

        wallCount = 0
        for i in [-1, 1]:
            if successor.hasWall(int(pos[0] + i), int(pos[1])):
                wallCount += 1
            if successor.hasWall(int(pos[0]), int(pos[1] + i)):
                wallCount += 1

        if wallCount == 3:
            return -9999

        actions = successor.getLegalActions(self.index)
        return 0.9 * max([self.depthLimitedSearchToHome(successor, action, depth + 1) for action in actions])

    def getSuccessor(self, gameState, action):
        # ?????? ???????????? ????????? ????????? ????????? ??? ?????? ????????? ??????
        successor = gameState.generateSuccessor(self.index, action)
        return successor
    

class DefensiveReflexAgent(CaptureAgent):
    def registerInitialState(self, gameState):
        self.start = gameState.getAgentPosition(self.index)
        CaptureAgent.registerInitialState(self, gameState)

        # ????????? ??? ????????? ????????? ?????? X ?????? ??????
        self.boundaryX = (gameState.data.layout.width - 2) // 2

        if not self.red:
            self.boundaryX += 1

        # ????????? ??? ????????? ????????? ?????? ?????? ?????? ??????
        self.boundaries = []
        for i in range(gameState.data.layout.height):
            if not gameState.hasWall(self.boundaryX, i):
                self.boundaries.append((self.boundaryX, i))

    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)

        # ?????? ???????????? ????????? ???????????? ????????? ??????
        values = [self.evaluate(gameState, action) for action in actions]

        # ?????? ??? ????????? ?????? ????????? ????????? ???????????? ??????
        maxValue = max(values)
        bestActions = [action for action, value in zip(actions, values) if value == maxValue]

        return random.choice(bestActions)

    def getSuccessor(self, gameState, action):
        # ?????? ???????????? ????????? ????????? ????????? ??? ?????? ????????? ??????
        successor = gameState.generateSuccessor(self.index, action)
        return successor

    def evaluate(self, gameState, action):
        # ?????? ????????? ????????? feature * weights??? linear combination?????? ??????
        features = self.getFeatures(gameState, action)
        weights = self.getWeights()
        return features * weights

    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)

        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # ????????? ?????? ??? ?????? invader??? ???
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [enemy for enemy in enemies if enemy.isPacman and enemy.getPosition() != None]
        features["numInvaders"] = len(invaders)

        # ????????? ????????? ??? ??? invader??? ??????????????? ?????? ????????? invader ????????? ??????
        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        # ????????? ????????? ??? ??? invader??? ??????, ????????? ?????? ?????? ????????? ?????? ?????? ?????? ????????? ??????????????? ??????
        else:
            deltaXCoord = self.boundaryX - myPos[0] if self.red else myPos[0] - self.boundaryX
            if deltaXCoord >= 0:
                features['nearBoundary'] = min([self.getMazeDistance(myPos, boundary) for boundary in self.boundaries])
            # invader??? ????????? ????????? ?????? ?????? ?????? ?????? ??? ????????? ???
            # ?????? ??????????????? ?????????????????? ?????? ??????????????? ?????? ?????????????????? ????????? ??????????????? ?????? ???????????? ????????? ???????????? ??????
            else:
                # ????????? ?????? ?????? 3??? ????????? ????????? ????????? ????????? ?????? ???
                if deltaXCoord >= -3:
                    features['nearBoundary'] = -1

        # ????????? ??????????????? ???????????? ?????? ????????? ????????? ?????? ?????? ??????
        # ????????? ????????? ????????? ?????? ?????? ????????? ?????? ????????? ???????????? ??????
        if myState.isPacman:
            enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
            ghosts = [enemy for enemy in enemies if
                      not enemy.isPacman and enemy.getPosition() is not None and enemy.scaredTimer == 0]

            if len(ghosts) > 0:
                dists = [self.getMazeDistance(myPos, ghost.getPosition()) for ghost in ghosts]
                if min(dists) <= 3:
                    features['nearGhost'] = min(dists)

        return features

    def getWeights(self):
        # invader??? ???/ invader????????? ?????? / boundary????????? ????????? ???????????? ???????????? ?????? weight
        # ????????? ????????? ?????? ???????????? ??????
        return {'numInvaders': -100, 'invaderDistance': -1, 'nearBoundary': -1, 'nearGhost': -1000}
