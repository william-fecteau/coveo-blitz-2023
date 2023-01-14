from game_message import *
from customMsg import *


def getNeighbours(gameMsg: GameMessage, teamId, pos: Position, range: int) -> List[Neighbour]:
    neighbours = list()
    for x in range(-range, range + 1):
        for y in range(-range, range + 1):
            if x == 0 and y == 0:
                continue

            curPos = Position(pos.x + x, pos.y + y)

            if isPosOutOfBound(curPos):
                continue

            curTile: Tile = gameMsg.playAreas[teamId].grid[curPos.x][curPos.y]

            neighbours.append(Neighbour(position=curPos, tile=curTile))

    return neighbours


def isPosOutOfBound(gameMsg: GameMessage, pos: Position):
    if pos.x >= gameMsg.map.width or pos.x < 0:
        return False
    if pos.y >= gameMsg.map.height or pos.y < 0:
        return False

    return True


def isCellEmpty(gameMsg: GameMessage, teamId, pos: Position):
    if isPosOutOfBound(pos):
        return False

    cell = gameMsg.playAreas[teamId].grid[pos.x][pos.y]

    return len(cell.enemies) == 0 and len(cell.towers) == 0 and len(cell.paths) == 0 and not cell.hasObstacle
