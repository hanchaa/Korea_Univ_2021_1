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

        # 자신의 팀 영역의 경계가 되는 X 좌표 계산
        self.boundaryX = (gameState.data.layout.width - 2) // 2

        if not self.red:
            self.boundaryX += 1

        # 자신의 팀 영역의 경계가 되는 모든 좌표 계산
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

        # 가장 큰 가치를 가진 액션들 중에서 랜덤하게 선택
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
            enemyDistance = min([self.getMazeDistance(agentState.getPosition(), enemy.getPosition()) for enemy in enemies if enemy.scaredTimer == 0], default=9999)

            if enemyDistance <= depth:
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

        if not agentState.isPacman:
            return 100

        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        enemyDistance = min(
            [self.getMazeDistance(agentState.getPosition(), enemy.getPosition()) for enemy in enemies])

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
        # 현재 상태에서 특정한 액션을 취했을 때 다음 상태를 생성
        successor = gameState.generateSuccessor(self.index, action)
        return successor
    

class DefensiveReflexAgent(CaptureAgent):
    def registerInitialState(self, gameState):
        self.start = gameState.getAgentPosition(self.index)
        CaptureAgent.registerInitialState(self, gameState)

        # 자신의 팀 영역의 경계가 되는 X 좌표 계산
        self.boundaryX = (gameState.data.layout.width - 2) // 2

        if not self.red:
            self.boundaryX += 1

        # 자신의 팀 영역의 경계가 되는 모든 좌표 계산
        self.boundaries = []
        for i in range(gameState.data.layout.height):
            if not gameState.hasWall(self.boundaryX, i):
                self.boundaries.append((self.boundaryX, i))

    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)

        # 현재 위치에서 가능한 액션들의 가치를 계산
        values = [self.evaluate(gameState, action) for action in actions]

        # 가장 큰 가치를 가진 액션들 중에서 랜덤하게 선택
        maxValue = max(values)
        bestActions = [action for action, value in zip(actions, values) if value == maxValue]

        return random.choice(bestActions)

    def getSuccessor(self, gameState, action):
        # 현재 상태에서 특정한 액션을 취했을 때 다음 상태를 생성
        successor = gameState.generateSuccessor(self.index, action)
        return successor

    def evaluate(self, gameState, action):
        # 어떤 액션의 가치를 feature * weights의 linear combination으로 계산
        features = self.getFeatures(gameState, action)
        weights = self.getWeights()
        return features * weights

    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)

        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # 액션을 하고 난 후의 invader의 수
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [enemy for enemy in enemies if enemy.isPacman and enemy.getPosition() != None]
        features["numInvaders"] = len(invaders)

        # 액션을 취하고 난 후 invader가 존재한다면 가장 가까운 invader 까지의 거리
        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        # 액션을 취하고 난 후 invader가 없고, 경계로 부터 멀리 떨어져 있을 경우 가장 가까운 경계까지의 거리
        else:
            if abs(myPos[0] - self.boundaryX) > 3:
                features['nearBoundary'] = min([self.getMazeDistance(myPos, boundary) for boundary in self.boundaries])
            # 만약 경계로 부터 일정 범위 내에 있다면 상대편 진영 쪽에 있는 것이 더 가치가 큼
            # 공격 에이전트가 경계에서 상대 에이전트에 의해 붙잡혀있다면 상대방 에이전트를 수비 에이전트 쪽으로 불러내기 위함
            else:
                if self.red:
                    features['nearBoundary'] = self.boundaryX - myPos[0] - 2
                else:
                    features['nearBoundary'] = myPos[0] - self.boundaryX - 2
                features['nearBoundary'] = max(features['nearBoundary'], -3)

        # 상대방 에이전트를 유도하기 위해 상대편 진영에 나가 있을 경우
        # 귀신이 가까운 거리로 오게 되는 행동은 하지 않도록 패널티를 부여
        if myState.isPacman:
            enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
            ghosts = [enemy for enemy in enemies if
                      not enemy.isPacman and enemy.getPosition() is not None and enemy.scaredTimer == 0]

            if len(ghosts) > 0:
                dists = [self.getMazeDistance(myPos, ghost.getPosition()) for ghost in ghosts]
                if min(dists) <= 3:
                    features['nearGhost'] = 1

        return features

    def getWeights(self):
        # invader의 수/ invader까지의 거리 / boundary까지의 거리는 작을수록 좋으므로 음의 weight
        # 경계를 넘어갈 경우 패널티를 부여
        return {'numInvaders': -100, 'invaderDistance': -1, 'nearBoundary': -1, 'nearGhost': -9999}
