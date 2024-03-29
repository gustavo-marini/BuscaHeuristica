# -*- coding: utf-8 -*-

from GraphMap import GraphMap
from GenerateMap import GenerateMap

def founded(founded, x, y):
    _founded = False
    for i, array in enumerate(founded):
        if array[0] == x and array[1] == y:
            _founded = True
    return _founded

if __name__ == '__main__':
    foundedGhosts = []

    graphMap = GraphMap()
    graphMap.setMapFile("mapa.txt").generateMapFromFile().setHunterAtMiddle().generateRandomGhosts()

    print("Mapa inicial")
    graphMap.printMap()

    firstMove = True

    while len(foundedGhosts) < graphMap.ghostCount:
        if firstMove:
            positions = graphMap.sweepInRadius(graphMap.hunterPosition[0], graphMap.hunterPosition[1])
            if len(positions) > 0:
                for rPos in positions:
                    if not founded(foundedGhosts, rPos[0], rPos[1]):
                        print("Fantasma encontrado dentro do raio de [x = %d, y = %d], nas coordenadas [x = %d, y = %d]" % (x, y, rPos[0], rPos[1]))
                        graphMap.moveTo(rPos[0], rPos[1])
                        foundedGhosts.append([rPos[0], rPos[1]])
        else:
            pos = graphMap.getNextPositionToMove()
            x = pos[0]
            y = pos[1]

            if graphMap.foundGhostInPosition(x, y) and not founded(foundedGhosts, x, y):
                print("Fantasma encontrado nas coordenadas [x = %d, y = %d]" % (x, y))
                graphMap.moveTo(x, y)
                foundedGhosts.append([x, y])

                positions = graphMap.sweepInRadius(x, y)
                if len(positions) > 0:
                    for rPos in positions:
                        if not founded(foundedGhosts, rPos[0], rPos[1]):
                            print(
                                "Fantasma encontrado dentro do raio de [x = %d, y = %d], nas coordenadas [x = %d, y = %d]" % (
                                x, y, rPos[0], rPos[1]))
                            graphMap.moveTo(rPos[0], rPos[1])
                            foundedGhosts.append([rPos[0], rPos[1]])
            elif len(graphMap.sweepInRadius(x, y)) > 0:
                positions = graphMap.sweepInRadius(x, y)
                for rPos in positions:
                    if not founded(foundedGhosts, rPos[0], rPos[1]):
                        print(
                            "Fantasma encontrado dentro do raio de [x = %d, y = %d], nas coordenadas [x = %d, y = %d]" % (
                            x, y, rPos[0], rPos[1]))
                        graphMap.moveTo(rPos[0], rPos[1])
                        foundedGhosts.append([rPos[0], rPos[1]])
            else:
                pass
                # print("Nenhum fantasma encontrado nas coordenadas [x = %d, y = %d] e dentro de seu raio" %(x, y))

        firstMove = False



    print("Movendo cacador para o meio do mapa...")
    graphMap.moveTo(19, 19)

    print("Custo total: %d" %graphMap.totalCost)

    #graphMap.printMap()
