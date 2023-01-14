from game_message import *
from actions import *
import random


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, gameMsg: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        self.gameMsg = gameMsg

        ourTeamId = gameMsg.teamId
        otherTeamIds = [team for team in gameMsg.teams if team != gameMsg.teamId]
        actions = list()
   

        curIndex = 0
        curTeam = 0

        if gameMsg.teamInfos[ourTeamId].money >= 200:
            pathPos: Position = gameMsg.map.paths[0].tiles[curIndex]
            neighboursPositions = self.getNeighbours(pathPos, 1)
            posIndex = random.randint(0, len(neighboursPositions) - 1)

            towerPos = neighboursPositions[posIndex]
            actions.append(BuildAction(TowerType.SPEAR_SHOOTER, towerPos))
            curIndex += 1
        else:
            actions.append(SendReinforcementsAction(EnemyType.LVL1, otherTeamIds[curTeam % len(otherTeamIds)]))
            curTeam += 1

        return actions

    def getNeighbours(self, pos: Position, range: int):
        neighbours = list()
        for x in range(-range, range + 1):
            for y in range(-range, range + 1):
                if x == 0 and y == 0:
                    continue

                checkX = pos.x + x
                checkY = pos.y + y
                
                if not self.isCellEmpty(self.gameMsg.teamId, Position(checkX, checkY)):
                    continue

                neighbours.append(Position(pos.x + x, pos.y + y))
        return neighbours


    def isCellOutOfBound(self, pos: Position):
        if self.gameMsg.map.width >= pos.x or pos.x < 0:
            return False
        if self.gameMsg.map.height >= pos.y or pos.y < 0:
            return False
        
        return True

    def isCellEmpty(self, teamId, pos: Position):
        if self.isCellOutOfBound(pos):
            return False

        cell = self.gameMsg.playAreas[teamId].grid[pos.x][pos.y]

        return len(cell.enemies) == 0 and len(cell.towers) == 0 and len(cell.paths) == 0