# myAgents.py
# ---------------
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

from game import Agent
from searchProblems import PositionSearchProblem

import util
import time
import search

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='ClosestDotAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

class MyAgent(Agent):
    """
    Implementation of your agent.
    """
    currentGoals = dict()  # 어떤 food가 어떤 agent에 의해 목표로 설정되어 있는지를 저장하는 static variable
    isGoalSet = dict()  # 어떤 agent의 목표 food가 설정되어 있는지 T/F를 저장하는 static variable

    def bfs(self, problem):
        queue = util.Queue()
        visited = dict()

        curState = [problem.getStartState(), [], 0]
        queue.push(curState)
        visited[curState[0]] = True

        while not queue.isEmpty():
            curState = queue.pop()

            if problem.isGoalState(curState[0]):
                if curState[0] not in self.currentGoals:  # search를 통해 찾아낸 가장 가까운 food가 다른 agent에 의해 목표로 설정되어 있지 않다면 현재 agent의 목표로 설정
                    self.currentGoals[curState[0]] = [self.index, curState[2]]  # [index, search를 통해 구한 현재 위치에서 food까지의 거리]를 저장
                    self.isGoalSet[self.index] = True
                    return curState[1]

                elif self.currentGoals[curState[0]][0] != self.index:  # search를 통해 찾아낸 가장 가까운 food가 다른 agent의 목표로 설정되어 있는 경우
                    if curState[2] - self.currentGoals[curState[0]][1] < -5:  # 이 food를 목표로 설정한 agent에서 food까지의 거리 - 현재 agent에서 food까지의 거리 > 5라면 현재 agent의 목표 food로 변경
                        self.isGoalSet[self.currentGoals[curState[0]][0]] = False
                        self.isGoalSet[self.index] = True
                        self.currentGoals[curState[0]] = [self.index, curState[2]]
                        return curState[1]

            for nextState in problem.getSuccessors(curState[0]):
                if nextState[0] not in visited:
                    route = curState[1].copy()
                    route.append(nextState[1])
                    queue.push([nextState[0], route, curState[2] + nextState[2]])
                    visited[nextState[0]] = True

        return ["Stop"]  # 적당한 food를 찾지 못했다면은 멈춰서 이동 패널티를 받지 않게 함

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        "*** YOUR CODE HERE ***"
        problem = AnyFoodSearchProblem(state, self.index)
        pos = problem.getStartState()

        if pos in self.currentGoals:  # 현재 위치가 어떤 agent에 의해 목표 된 곳이면 목표 목록에서 제거해준다
            self.isGoalSet[self.currentGoals[pos][0]] = False
            del self.currentGoals[pos]

        if self.isDone:  # 남은 food가 다른 agent들에게 모두 할당 되고 남은게 없을 경우 이동하지 않음
            return "Stop"

        if self.isGoalSet[self.index] and len(self.savedRoute) > 0:  # 현재 에이전트의 목표가 있고 저장된 경로가 존재한다면 bfs를 하지 않고 저장된 경로를 이용
            for i in self.currentGoals.keys():  # 목표 목록에 저장된 각 에이전트에서 목표까지 남은 거리 업데이트
                if self.currentGoals[i][0] == self.index:
                    self.currentGoals[i][1] -= 1
                    break
            return self.savedRoute.pop(0)

        self.savedRoute = self.bfs(problem)
        action = self.savedRoute.pop(0)

        if action == "Stop":
            self.isDone = True

        return action

    def initialize(self):
        self.isGoalSet[self.index] = False
        self.savedRoute = []
        self.isDone = False

"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)


        "*** YOUR CODE HERE ***"

        pacmanCurrent = [problem.getStartState(), [], 0]
        visitedPosition = set()
        # visitedPosition.add(problem.getStartState())
        fringe = util.PriorityQueue()
        fringe.push(pacmanCurrent, pacmanCurrent[2])
        while not fringe.isEmpty():
            pacmanCurrent = fringe.pop()
            if pacmanCurrent[0] in visitedPosition:
                continue
            else:
                visitedPosition.add(pacmanCurrent[0])
            if problem.isGoalState(pacmanCurrent[0]):
                return pacmanCurrent[1]
            else:
                pacmanSuccessors = problem.getSuccessors(pacmanCurrent[0])
            Successor = []
            for item in pacmanSuccessors:  # item: [(x,y), 'direction', cost]
                if item[0] not in visitedPosition:
                    pacmanRoute = pacmanCurrent[1].copy()
                    pacmanRoute.append(item[1])
                    sumCost = pacmanCurrent[2]
                    Successor.append([item[0], pacmanRoute, sumCost + item[2]])
            for item in Successor:
                fringe.push(item, item[2])
        return pacmanCurrent[1]

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        if self.food[x][y] == True:
            return True
        return False

