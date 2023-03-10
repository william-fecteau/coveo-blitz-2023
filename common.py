from game_message import *
import random


def getNeighbours(gameMsg: GameMessage, position: Position) -> list[Neighbour]:
    neighbours = list()
    for x in range(position.x - 1, position.x + 2):
        for y in range(position.y - 1, position.y + 2):
            if x < 0 or y < 0 or x >= gameMsg.map.width or y >= gameMsg.map.height:
                continue
            if x == position.x and y == position.y:
                continue

            grid = gameMsg.playAreas[gameMsg.teamId].grid
            tile = None
            if x in grid:
                if y in grid[x]:
                    tile = grid[x][y]

            neighbours.append(Neighbour(Position(x, y), tile))

    return neighbours


def isTileEmpty(tile: Tile):
    return tile is None or (len(tile.paths) == 0 and len(tile.towers) == 0 and len(tile.enemies) == 0 and not tile.hasObstacle)


def positionRandom(gameMsg: GameMessage):
    return Position(random.randint(0, gameMsg.map.width - 1), random.randint(0, gameMsg.map.height - 1))


def countTowerType(gameMsg: GameMessage, towerType: TowerType):
    typeCount = 0
    for tower in gameMsg.playAreas[gameMsg.teamId].towers:
        if tower.type == towerType:
            typeCount += 1
    return typeCount
