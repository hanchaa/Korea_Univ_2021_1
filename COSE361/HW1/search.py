# search.py
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    route = {} # goal state를 찾은 후 지나온 경로를 backtracking 하기 위한 dictionary
    res = [] # goal state 까지의 경로 저장 배열

    start = problem.getStartState()
    backtrack = start
    is_goal = problem.isGoalState(start) # 시작 위치가 goal state인지 확인

    stack.push((start, "", 0, -1)) # 시작 위치를 stack에 넣은 후 탐색 시작
                                   # 스택에는 (다음 위치, 이동 방법, 이동 비용, 현재 위치)로 이루어진 tuple을 push

    while not (stack.isEmpty() or is_goal):
        cur_state = stack.pop() # stack에서 pop 된 node를 현재 위치로 설정

        if cur_state[0] in route: # 이미 방문한 node인 경우 expand를 하지 않음
            continue

        route[cur_state[0]] = {"from": cur_state[3], "by": cur_state[1]} # 방문한 node라고 표시해주고 어디서 어떻게 왔는지 저장

        is_goal = problem.isGoalState(cur_state[0]) # 현재 노드가 goal state인지 확인 후 그렇다면은 백트래킹을 위해 goal의 위치를 저장 후 탐색 종료
        if is_goal:
            backtrack = cur_state[0]
            break

        for next_state in problem.getSuccessors(cur_state[0]): # 현재 위치에서 node expand 해서 다음으로 갈 수 있는 fringe들을 stack에 push
            stack.push(next_state + (cur_state[0], ))

    while backtrack != start: # route dictionary를 이용해 goal 위치에서 부터 시작 위치로 backtracking 하면서 res 배열에 경로 저장
        res.insert(0, route[backtrack]["by"])
        backtrack = route[backtrack]["from"]

    return res


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    route = {} # goal state를 찾은 후 지나온 경로를 backtracking 하기 위한 dictionary
    res = [] # goal state 까지의 경로 저장 배열

    start = problem.getStartState()
    backtrack = start
    is_goal = problem.isGoalState(start) # 시작 위치가 goal state인지 확인

    queue.push((start, "", 0, -1)) # 시작 위치를 큐에 넣은 후 탐색 시작
                                   # 큐에는 (다음 위치, 이동 방법, 이동 비용, 현재 위치)로 이루어진 tuple을 push

    while not (queue.isEmpty() or is_goal):
        cur_state = queue.pop() # stack에서 pop 된 node를 현재 위치로 설정

        if cur_state[0] in route: # 이미 방문한 node인 경우 expand를 하지 않음
            continue

        route[cur_state[0]] = {"from": cur_state[3], "by": cur_state[1]} # 방문한 node라고 표시해주고 어디서 어떻게 왔는지 저장

        is_goal = problem.isGoalState(cur_state[0]) # 현재 노드가 goal state인지 확인 후 그렇다면은 백트래킹을 위해 goal의 위치를 저장 후 탐색 종료
        if is_goal:
            backtrack = cur_state[0]
            break

        for next_state in problem.getSuccessors(cur_state[0]): # 현재 위치에서 node expand 해서 다음으로 갈 수 있는 fringe들을 큐에 push
            queue.push(next_state + (cur_state[0], ))

    while backtrack != start: # route dictionary를 이용해 goal 위치에서 부터 시작 위치로 backtracking 하면서 res 배열에 경로 저장
        res.insert(0, route[backtrack]["by"])
        backtrack = route[backtrack]["from"]

    return res


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pq = util.PriorityQueue()
    route = {}  # goal state를 찾은 후 지나온 경로를 backtracking 하기 위한 dictionary
    res = []  # goal state 까지의 경로 저장 배열

    start = problem.getStartState()
    backtrack = start
    is_goal = problem.isGoalState(start) # 시작 위치가 goal state인지 확인

    pq.push((start, "", 0, -1), 0) # 시작 위치를 우선순위 큐에 넣은 후 탐색 시작
                                   # 우선순위 큐에는 (다음 위치, 이동 방법, 누적 비용, 현재 위치)로 이루어진 tuple이 들어가며 priority는 start로 부터 다음 위치까지 가는데 필요한 누적 비용으로 계산

    while not (pq.isEmpty() or is_goal):
        cur_state = pq.pop() # 우선순위 큐에서 pop 된 노드를 현재 노드로 설정

        if cur_state[0] in route: # 이미 방문한 노드인 경우 expand를 수행하지 않음
            continue

        route[cur_state[0]] = {"from": cur_state[3], "by": cur_state[1]} # 방문한 노드라고 표시 후 어디서 어떻게 왔는지 저장

        is_goal = problem.isGoalState(cur_state[0]) # 현재 노드가 goal state인지 확인 후 그렇다면은 backtracking을 위해 현재 노드 저장 후 탐색 종료
        if is_goal:
            backtrack = cur_state[0]
            break

        for next_state in problem.getSuccessors(cur_state[0]): # 현재 위치에서 node expand 해서 다음으로 갈 수 있는 fringe들을 우선순위 큐에 push
            accumulated_cost = cur_state[2] + next_state[2] # 현재 노드까지 오는데 사용한 cost와 다음 노드로 이동하는데 필요한 cost를 더해서 다음 노드까지의 accumulated cost를 구함
            pq.push((next_state[0], next_state[1], accumulated_cost, cur_state[0]), accumulated_cost)

    while backtrack != start: # route dictionary를 이용해 goal 위치에서 부터 시작 위치로 backtracking 하면서 res 배열에 경로 저장
        res.insert(0, route[backtrack]["by"])
        backtrack = route[backtrack]["from"]

    return res


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pq = util.PriorityQueue()
    route = {}  # goal state를 찾은 후 지나온 경로를 backtracking 하기 위한 dictionary
    res = []  # goal state 까지의 경로 저장 배열

    start = problem.getStartState()
    backtrack = start
    is_goal = problem.isGoalState(start) # 시작 위치가 goal state인지 확인
    forward_cost = heuristic(start, problem) # priority 계산에 필요한 forward cost를 heuristic을 이용해 계산

    pq.push((start, "", 0, -1), 0 + forward_cost) # 시작 위치를 우선순위 큐에 넣은 후 탐색 시작
                                                  # 우선순위 큐에는 (다음 위치, 이동 방법, 누적 비용, 현재 위치)로 이루어진 tuple이 들어가며 priority는 backward cost와 forward cost를 더한 값으로 사용

    while not (pq.isEmpty() or is_goal):
        cur_state = pq.pop() # 우선순위 큐에서 pop한 값을 현재 노드로 설정

        if (cur_state[0] in route): # 이미 방문한 노드라면 expand를 실행하지 않음
            continue

        route[cur_state[0]] = {"from": cur_state[3], "by": cur_state[1]} # 방문한 노드로 표시 후 어디서 어떻게 왔는지 저장

        is_goal = problem.isGoalState(cur_state[0]) # 현재 노드가 goal state인지 확인후, 그렇다면 백트래킹을 위해 goal state의 위치를 저장 후 탐색 종료
        if is_goal:
            backtrack = cur_state[0]
            break

        for next_state in problem.getSuccessors(cur_state[0]): # 현재 위치에서 node expand 해서 다음으로 갈 수 있는 fringe들을 우선순위 큐에 push
            backward_cost = cur_state[2] + next_state[2] # backward cost는 현재 노드까지 오는데 사용한 비용과 다음 노드로 이동하는데 필요한 비용을 더해서 구한다
            forward_cost = heuristic(next_state[0], problem) # forward cost는 heuristic을 이용해 다음 노드에서 골 노드까지의 거리를 이용해서 구한다
            pq.push((next_state[0], next_state[1], backward_cost, cur_state[0]), backward_cost + forward_cost)

    while backtrack != start: # route dictionary를 이용해 goal 위치에서 부터 시작 위치로 backtracking 하면서 res 배열에 경로 저장
        res.insert(0, route[backtrack]["by"])
        backtrack = route[backtrack]["from"]

    return res


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
