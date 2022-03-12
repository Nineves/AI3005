import math
import sys
from queue import PriorityQueue

class Node:

  def __init__(self, name, parent, distFromSrc):
    self.name = name                #a string
    self.parent = parent
    self.distFromSrc = distFromSrc
    self.budget = 999999

  def heuristic(self, coord):
    distFromEnd = math.sqrt((coord["50"][0]-coord[self.name][0])**2 + (coord["50"][1]-coord[self.name][1])**2)
    return distFromEnd + self.distFromSrc

  def setBudget(self, setBudget):
    self.budget = setBudget

  def __eq__(self, other):
    return (self.name == other.name) and (self.distFromSrc == other.distFromSrc)

  def __ne__(self, other):
    return not (self == other)

  def __lt__(self, other):
    return (self.name < other.name) and (self.distFromSrc < other.distFromSrc)

  def __gt__(self, other):
    return (self.name > other.name) and (self.distFromSrc > other.distFromSrc)

  def __le__(self, other):
    return (self < other) or (self == other)

  def __ge__(self, other):
    return (self > other) or (self == other)

class AStarSearch:

    def __init__(self, Cost, Dist, G, Coord):
        self.G = G
        self.Cost = Cost
        self.Dist = Dist
        self.REMOVED = '<removed-task>'  # placeholder for a removed task
        self.DEFAULT_DISTANCE = sys.maxsize
        self.distFromSrc = [self.DEFAULT_DISTANCE] * (len(G) + 1)
        self.pq = PriorityQueue()
        self.EF = dict()
        self.budgetFromSrc = [0] * (len(self.G) + 1)
        self.visited = dict()
        self.Coord = Coord


    def printPath(self, path, end):
        print("Shortest path: ", end='')
        for node in reversed(path):
            if (node == end):
                print(node)
            else:
                print(node, "->", end='')

    def calcEnergy(self,path):
        i = 0
        energy = 0
        while (i < len(path) - 1):
            energy = self.Cost[(path[i] + "," + path[i + 1])]
            i = i + 1
        return energy

    def getAStarPath(self, path, start, end):
        reversedPath = []
        initialNode = path[-1]
        reversedPath.append(initialNode.name)
        preNode = initialNode.parent

        while (preNode.name != start):
            reversedPath.append(preNode.name)
            preNode = preNode.parent

        reversedPath.append(start)

        self.printPath(reversedPath, end)
        print("Shortest Distance: ", initialNode.distFromSrc)
        print("Total Energy Cost: ", initialNode.budget)


    def AStarSearchProcess(self, start, end):
        ENERGY_BUDGET = 287932
        curPath = []
        visitedBudget = dict()
        srcNode = Node(start, None, 0)
        srcNode.setBudget(0)
        self.visited[start] = srcNode.heuristic(self.Coord)
        visitedBudget[start] = 0
        curPath.append(srcNode)

        for node in self.G[start]:
            newNode = Node(node, srcNode, srcNode.distFromSrc + self.Dist[start + ',' + node])
            newNode.setBudget(self.Cost[srcNode.name + "," + newNode.name] + srcNode.budget)
            FCost = newNode.heuristic(self.Coord)
            self.pq.put((FCost, newNode))
        # print(pq)

        while not self.pq.empty():
            newNode = self.pq.get()[1]
            if (newNode.name in self.visited and newNode.heuristic(self.Coord) >= self.visited[newNode.name] and newNode.budget >=
                    visitedBudget[newNode.name]):
                continue
            curPath.append(newNode)
            if newNode.name in self.visited:
                if newNode.heuristic(self.Coord) < self.visited[newNode.name]:
                    self.visited[newNode.name] = newNode.heuristic(self.Coord)
                if newNode.budget < visitedBudget[newNode.name]:
                    visitedBudget[newNode.name] = newNode.budget
            else:  # the node has not been expanded before
                self.visited[newNode.name] = newNode.heuristic(self.Coord)
                visitedBudget[newNode.name] = newNode.budget
            if newNode.name == end:
                print("Search ended.")
                break

            for adjNode in self.G[newNode.name]:

                distFromSrc = newNode.distFromSrc + self.Dist[newNode.name + "," + adjNode]
                adjNewNode = Node(adjNode, newNode, distFromSrc)
                FValue = adjNewNode.heuristic(self.Coord)
                curBudget = newNode.budget + self.Cost[newNode.name + "," + adjNewNode.name]
                # print("adjNode ", adjNode)
                # print("budget ", curBudget)
                if curBudget >= ENERGY_BUDGET:
                    continue
                adjNewNode.setBudget(curBudget)
                self.pq.put((FValue, adjNewNode))
        return curPath

    def Astar(self, start, end):
        path = self.AStarSearchProcess(start, end)
        self.getAStarPath(path, start, end)


