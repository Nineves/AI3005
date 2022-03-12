from heapq import heapify, heappush, heappop
import sys

class Dijkstra:
    DEFAULT_DISTANCE = sys.maxsize
    def __init__(self, Cost, Dist, G):
        self.DEFAULT_DISTANCE = sys.maxsize
        self.G = G
        self.Cost = Cost
        self.Dist = Dist
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        self.distFromSrc = [self.DEFAULT_DISTANCE] * (len(G) + 1)
        self.pre = []
        self.pq = []
        self.EF = dict()
        self.visited = []


    def findShortestPath(self, start, end):
        self.pre = ["0"] * (len(self.G)+1)
        visited = [0] * (len(self.G) + 1)
        self.distFromSrc[int(start)] = 0
        visited[int(start)] = 1
        for node in self.G[start]:
            if (self.distFromSrc[int(node)] > self.distFromSrc[int(start)] + self.Dist[start + ',' + node]):
                self.distFromSrc[int(node)] = self.distFromSrc[int(start)] + self.Dist[start + ',' + node]
                self.pre[int(node)] = start
                self.add_node(node,self.distFromSrc[int(node)])

        while (len(self.pq) > 0):
            newNode = self.pop_node(self.EF)
            visited[int(newNode)] = 1
            for adjNode in self.G[newNode]:
                if (self.distFromSrc[int(adjNode)] > self.distFromSrc[int(newNode)] + self.Dist[newNode + "," + adjNode] and (visited[int(adjNode)] == 0)):
                    self.distFromSrc[int(adjNode)] = self.distFromSrc[int(newNode)] + self.Dist[newNode + "," + adjNode]
                    self.pre[int(adjNode)] = newNode
                    self.add_node(adjNode, self.distFromSrc[int(adjNode)])
        self.getPath(start, end)



    def getPath(self, start, end):
        path_reversed = []
        prevNode = self.pre[int(end)]
        if(prevNode == "-1"):
            print("Path not found.")
            return
        path_reversed.append(end)
        while (prevNode != start):
            path_reversed.append(prevNode)
            prevNode = self.pre[int(prevNode)]
        path_reversed.append(start)

        self.printPath(path_reversed, end)
        energy = self.calcEnergy(path_reversed)

        print("Shortest distance:", self.distFromSrc[int(end)])
        print("Total energy cost:", energy)

    def add_node(self, node,dist):
        if node in self.EF:
            self.remove_node(node, self.EF)
        entry = [dist, node]
        self.EF[node] = entry
        heappush(self.pq, entry)

    def remove_node(self, task, entry_finder):
        entry = entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_node(self,entry_finder):
        while self.pq:
            dist, node = heappop(self.pq)
            if node is not self.REMOVED:
                del entry_finder[node]
                return node
        raise KeyError('pop from an empty priority queue')

    def printPath(self, path, dest):
        print("Shortest path: ", end='')
        for node in reversed(path):
            if (node == dest):
                print(node)
            else:
                print(node, "->", end='')

    def calcEnergy(self, path):
        i = 0
        energy = 0
        while (i < len(path) - 1):
            energy = self.Cost[(path[i] + "," + path[i + 1])] + energy
            i = i + 1
        return energy




