import random
from sty import fg, bg, RgbFg
from AStar import AStar


class GraphMap:

    def __init__(self):
        self.types = []
        self.mapSizeX = 42
        self.mapSizeY = 42
        self.map = [[" "] * self.mapSizeX for _ in range(self.mapSizeY)]
        self.original_map = [[" "] * self.mapSizeX for _ in range(self.mapSizeY)]
        self.path_map = [[" "] * self.mapSizeX for _ in range(self.mapSizeY)]
        self.ghost = {
            "name": "Ghost",
            "symbol": "F",
            "color": (255, 0, 0)
        }
        self.hunterRadius = {
            "name": "Hunter Radius",
            "symbol": "R",
            "color": (255, 70, 0)
        }
        self.radiusSize = 3
        self.radiusPosition = []
        self.ghostCount = 6
        self.hunter = {
            "name": "Hunter",
            "symbol": "H",
            "color": (255, 255, 0)
        }
        self.ghostPositions = []
        self.hunterPosition = []
        self.validDirections = ["up", "down", "left", "right"]
        self.mapFile = None
        self.visitedPoints = []
        self.totalCost = 0
        self.mountTypes()

    def mountTypes(self):
        waterType = {
            "name": "Water",
            "symbol": "W",
            "cost": 12,
            "color": (0, 119, 190)
        }
        grassType = {
            "name": "Grass",
            "symbol": "G",
            "cost": 1,
            "color": (124, 252, 0)
        }
        mountainType = {
            "name": "Mountain",
            "symbol": "M",
            "cost": 70,
            "color": (151, 124, 83)
        }

        self.types.append(waterType)
        self.types.append(grassType)
        self.types.append(mountainType)

    def getTypeBy(self, key, value):
        for type in self.types:
            if type[key] == value:
                return type
        return None

    def neighbors(self, pos):
        (x, y) = pos
        positions = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        results = []
        for p in positions:
            if self.isValidPoint(p[0], p[1]):
                results.append((p[0], p[1]))
        return results

    def getNoiseMap(self):
        noise_map = []

        for y in range(self.mapSizeX):
            new_row = []
            for x in range(self.mapSizeY):
                new_row.append(0)
            noise_map.append(new_row)

        top_of_range = 0
        bottom_of_range = 0
        for y in range(self.mapSizeX):
            for x in range(self.mapSizeY):
                if x == 0 and y == 0:
                    continue
                if y == 0:
                    new_value = noise_map[y][x - 1] + random.randint(-1000, +1000)
                elif x == 0:
                    new_value = noise_map[y - 1][x] + random.randint(-1000, +1000)
                else:
                    minimum = min(noise_map[y][x - 1], noise_map[y - 1][x])
                    maximum = max(noise_map[y][x - 1], noise_map[y - 1][x])
                    average_value = minimum + ((maximum - minimum) / 2.0)
                    new_value = average_value + random.randint(-1000, +1000)
                noise_map[y][x] = new_value

                if new_value < bottom_of_range:
                    bottom_of_range = new_value
                elif new_value > top_of_range:
                    top_of_range = new_value

        difference = float(top_of_range - bottom_of_range)
        for y in range(self.mapSizeX):
            for x in range(self.mapSizeY):
                noise_map[y][x] = (noise_map[y][x] - bottom_of_range) / difference
        return noise_map

    def generateRandomMap(self, return_map=False):
        noise_map = self.getNoiseMap()

        for row in noise_map:
            for i, cell in enumerate(row):
                if cell < 0.3:
                    row[i] = "W"
                elif cell < 0.6:
                    row[i] = "G"
                else:
                    row[i] = "M"

        self.map = noise_map
        self.original_map = noise_map
        self.path_map = noise_map

        if return_map:
            return self.map
        return self

    def setMapFile(self, file):
        self.mapFile = file
        return self

    def generateMapFromFile(self):
        if self.mapFile:
            map = []

            for y in range(self.mapSizeX):
                new_row = []
                for x in range(self.mapSizeY):
                    new_row.append(0)
                map.append(new_row)

            file = open(self.mapFile, "rb")
            for i, line in enumerate(file.readlines()):
                line = line.decode("utf-8")
                for j, char in enumerate(line):
                    if i < self.mapSizeX and j < self.mapSizeY:
                        map[i][j] = char.upper()
                        self.map[i][j] = char.upper()
                        self.original_map[i][j] = char.upper()
                        self.path_map[i][j] = char.upper()
        return self

    def setHunterAtMiddle(self):
        #x = int(self.mapSizeX / 2)
        #y = int(self.mapSizeY / 2)
        x = 19
        y = 19
        self.map[x][y] = self.hunter["symbol"]
        self.path_map[x][y] = self.hunter["symbol"]
        self.hunterPosition = [x, y]
        return self

    def generateRandomGhosts(self):
        ghostPositions = []
        for y in range(self.ghostCount):
            ghostPositions.append([0, 0])

        for i in range(0, self.ghostCount):
            x = random.randint(0, 41)
            y = random.randint(0, 41)
            while self.map[x][y] == self.ghost["symbol"] or self.map[x][y] == self.hunter["symbol"]:
                x = random.randint(0, 41)
                y = random.randint(0, 41)
            self.map[x][y] = self.ghost["symbol"]
            self.path_map[x][y] = self.ghost["symbol"]
            self.ghostPositions.append([x, y])

        return self

    def isValidPoint(self, x, y):
        return 0 <= x < self.mapSizeX and 0 <= y < self.mapSizeY

    def setHunterRadius(self):
        x = self.hunterPosition[0]
        y = self.hunterPosition[1]
        for i in range(x - self.radiusSize, x + self.radiusSize + 1):
            for j in range(y - self.radiusSize, y + self.radiusSize + 1):
                if self.isValidPoint(i, j):
                    if self.map[i][j] != self.ghost["symbol"] and self.map[i][j] != self.hunter["symbol"]:
                        self.radiusPosition.append([i, j])
                        #self.map[i][j] = self.hunterRadius["symbol"]

    def visistedPoint(self, x, y):
        for index, array in enumerate(self.visitedPoints):
            if array[0] == x and array[1] == y:
                return True
        return False

    def getNextPositionToMove(self):
        x = -1
        y = -1

        while not self.isValidPoint(x, y) and not self.visistedPoint(x, y):
            x = random.randint(0, self.mapSizeX - 1)
            y = random.randint(0, self.mapSizeY - 1)

        self.visitedPoints.append([x, y])
        nextPosition = [x, y]
        return nextPosition

    def moveTo(self, x, y):
        next_position = [x, y]

        a_star = AStar()

        (start, goal) = (self.hunterPosition[0], self.hunterPosition[1]), (next_position[0], next_position[1])
        path, cost = a_star.search(self, start, goal)

        #self.map[self.hunterPosition[0]][self.hunterPosition[1]] = self.original_map[self.hunterPosition[0]][self.hunterPosition[1]]
        self.hunterPosition = [goal[0], goal[1]]
        #self.map[x][y] = self.hunter["symbol"]
        #self.path_map[x][y] = self.hunter["symbol"]

        self.totalCost += cost

        print("Caminho: [%d, %d] -> [%d, %d]" %(start[0], start[1], goal[0], goal[1]), end="\n")
        print("Custo: %d" %cost)
        print("Custo ate o momento: %d\n" %self.totalCost)

        for i, p in enumerate(path):
            if p:
                if i == len(path) - 1:
                    self.path_map[p[0]][p[1]] = "H"
                else:
                    self.path_map[p[0]][p[1]] = "P"
        self.printMap()
        for i, p in enumerate(path):
            if p:
                if i == len(path) - 1:
                    self.path_map[p[0]][p[1]] = "H"
                else:
                    self.path_map[p[0]][p[1]] = self.original_map[p[0]][p[1]]

        return self

    def foundGhostInPosition(self, x, y):
        for ghost in self.ghostPositions:
            if ghost[0] == x and ghost[1] == y:
                return True
        return False

    def sweepInRadius(self, x, y):
        positions = []
        for i in range(x - self.radiusSize, x + self.radiusSize + 1):
            for j in range(y - self.radiusSize, y + self.radiusSize + 1):
                if self.isValidPoint(i, j):
                    if self.map[i][j] == self.ghost["symbol"]:
                        positions.append([i, j])
        return positions

    def printMap(self):
        fg.set_style('water', RgbFg(0, 119, 190))
        fg.set_style('grass', RgbFg(124, 252, 0))
        fg.set_style('mountain', RgbFg(151, 124, 83))
        fg.set_style('hunter', RgbFg(255, 255, 0))
        fg.set_style('ghost', RgbFg(255, 0, 0))
        fg.set_style('radius', RgbFg(255, 70, 0))
        fg.set_style('console', RgbFg(255, 255, 255))

        for row in self.path_map:
            for i, cell in enumerate(row):
                if cell == "W":
                    print(fg.water + cell, end=" ")
                elif cell == "G":
                    print(fg.grass + cell, end=" ")
                elif cell == "M":
                    print(fg.mountain + cell, end=" ")
                elif cell == "H":
                    print(fg.hunter + cell, end=" ")
                elif cell == "F":
                    print(fg.ghost + cell, end=" ")
                elif cell == "R":
                    print(fg.radius + cell, end=" ")
                elif cell == "P":
                    print(fg.radius + cell, end=" ")
            print(fg.console + "", end="\n")
        print("\n\n\n")
