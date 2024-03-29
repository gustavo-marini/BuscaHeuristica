from PriorityQueue import PriorityQueue

class AStar:
    def __init__(self):
        self.frontier = PriorityQueue()

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def search(self, graph, start, goal):
        self.frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not self.frontier.empty():
            current = self.frontier.get()

            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path, cost_so_far[goal]

            for next in graph.neighbors(current):
                tile = graph.original_map[next[0]][next[1]]
                cost = graph.getTypeBy("symbol", tile)["cost"]
                new_cost = cost_so_far[current] + cost
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    self.frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far
