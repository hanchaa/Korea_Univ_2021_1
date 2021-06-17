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
from util import nearestPoint


#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='PessimisticReflexAgent', second='DefensiveReflexAgent'):
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

class ReflexCaptureAgent(CaptureAgent):
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
        features['successorScore'] = self.getScore(successor)
        return features

    def getWeights(self):
        return {'successorScore': 1.0}


class PessimisticReflexAgent(ReflexCaptureAgent):
    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)

        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # 하나라도 food를 먹은 상태라면 집으로 돌아오도록 feature를 설정
        if gameState.getAgentState(self.index).numCarrying >= 1:
            features['distToHome'] = min([self.getMazeDistance(myPos, boundary) for boundary in self.boundaries])

        # food를 먹지 못했다면은 food 가장 가까운 food를 찾도록 feature를 설정
        else:
            # 액션을 취한 후 food의 개수
            foodList = self.getFood(successor).asList()
            features['foodLeft'] = len(foodList)

            # 액션을 취한 후 가장 가까운 food까지의 거리
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distToFood'] = minDistance

        # 가장 가까운 ghost까지의 거리 계산
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        ghosts = [enemy for enemy in enemies if
                  not enemy.isPacman and enemy.getPosition() is not None and enemy.scaredTimer == 0]

        if len(ghosts) > 0:
            dists = [self.getMazeDistance(myPos, ghost.getPosition()) for ghost in ghosts]
            # 가장 가까운 ghost까지의 거리가 멀 때는 큰 영향을 끼치지 않지만 가까워질수록 그 영향이 커지도록 반비례 관계
            features['distToGhost'] = 1 / min(dists)

            # 어떤 행동의 결과 고스트에게 잡혀 원래 위치로 돌아가게 된다면 그 방향으로 가지 않게 큰 패널티를 줌
            if myPos == self.start:
                features['distanceToGhost'] = 9999

        return features

    def getWeights(self):
        # foodLeft / distToFood / distToHome은 작을수록 좋으므로 음수
        # distToGhost는 feature가 이미 반비례 관계이므로 적당한 weight만 적용
        return {'foodLeft': -100, 'distToFood': -1, 'distToGhost': -15, 'distToHome': -1}


class DefensiveReflexAgent(ReflexCaptureAgent):
    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)

        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # 액션을 하고 난 후의 invader의 수
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [enemy for enemy in enemies if enemy.isPacman and enemy.getPosition() != None]
        features["numInvaders"] = len(invaders)

        # 액션을 취했을 때 경계선을 넘어가는지 여부
        if myState.isPacman or myPos == self.start:
            features["crossBoundary"] = 1

        # 액션을 취하고 난 후 invader가 존재한다면 가장 가까운 invader 까지의 거리
        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        # 액션을 취하고 난 후 invader가 없고, 경계로 부터 멀리 떨어져 있을 경우 가장 가까운 경계까지의 거리
        elif abs(myPos[0] - self.boundaryX) > 4:
            features['nearBoundary'] = min([self.getMazeDistance(myPos, boundary) for boundary in self.boundaries])

        return features

    def getWeights(self):
        # invader의 수/ invader까지의 거리 / boundary까지의 거리는 작을수록 좋으므로 음의 weight
        # 경계를 넘어갈 경우 패널티를 부여
        return {'numInvaders': -100, 'crossBoundary': -1, 'invaderDistance': -1, 'nearBoundary': -1}
