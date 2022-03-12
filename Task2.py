class BFS:
    # '1' is start node and energy = 0
    # Dictionary format
    # {Child Node: [Parent Node, Child Node's Distance From Start, Child Node's Energy from Start]}
    def __init__(self, Cost, Dist, G, budget):
        self.G = G
        self.Cost = Cost
        self.Dist = Dist
        self.queue = ['1']
        self.BFS_tree = {'1': ['1', 0, 0]}
        self.set_visited = set([])
        self.budget = budget

    def explore_nodes(self, G, Dist, Cost, budget):

        # Get current node from queue
        cur_node = self.queue.pop(0)
        # Set current node as visited
        self.set_visited.add(cur_node)

        # check current node's neighbour
        # if node's neighbour visited before, skip
        # else calculate their cost

        for child_node in G[cur_node]:
            if child_node in self.set_visited:
                continue
            else:
                self.calculate_Cost(cur_node, child_node, Dist, Cost, budget)

    def calculate_Cost(self, cur_node, child_node, Dist, Cost, budget):

        # Current Node's (Parent) total distance from start node
        parent_dist_from_start = self.BFS_tree[cur_node][1]
        # Current Node's (Parent) total energy from start node
        parent_energy_from_start = self.BFS_tree[cur_node][2]

        # Child Node's total distance from '1'
        child_dist_from_start = parent_dist_from_start + Dist[cur_node + ',' + child_node]
        # Child Node's total energy from '1'
        child_energy_from_start = parent_energy_from_start + Cost[cur_node + ',' + child_node]

        # If current node's total energy + child node's energy <= budget, update tree
        if child_energy_from_start <= budget:

            # unexplored node
            # update to tree
            if child_node not in self.BFS_tree.keys():
                self.BFS_tree[child_node] = [cur_node, child_dist_from_start, child_energy_from_start]

            # explored node
            else:
                child_dist_in_tree = self.BFS_tree[child_node][1]

                # Update tree to take minimum distance
                if child_dist_from_start < child_dist_in_tree:
                    self.BFS_tree[child_node] = [cur_node, child_dist_from_start, child_energy_from_start]

            # append to queue the queue for visiting, if child node is not yet queued
            if child_node not in self.queue:
                self.queue.append(child_node)

    # Backtrack shortest path after calculating
    def backtrack(self, start, end, tree):

        # Starting from end node
        path = [end]
        cur_node = end
        parent_node = tree[cur_node][0]

        # Keep retrieving parent node until current node is start node
        while cur_node != start:
            path.insert(0, parent_node)
            cur_node = parent_node
            parent_node = tree[cur_node][0]

        return path

    def template(self, start, end):
        while self.queue:
            # print("nodes visited = ", len(set_visited),end = '\r',)
            self.explore_nodes(self.G, self.Dist, self.Cost, self.budget)
        path = start
        backtrackPath = self.backtrack(start, end, self.BFS_tree)
        for node in backtrackPath:
            if node == "1":
                continue
            else:
                path += ("->" + node)

        dist_to_dest = self.BFS_tree[end][1]

        print("ShortestPath: ", path)
        print("Shortest distance: ", dist_to_dest)
        print("Total energy cost: ", self.BFS_tree[end][2])

        return path