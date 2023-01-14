from game_message import *


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
            if position.x in grid:
                if position.y in grid[position.x]:
                    tile = grid[position.x][position.y]

            neighbours.append(Neighbour(Position(x, y), tile))

    return neighbours
