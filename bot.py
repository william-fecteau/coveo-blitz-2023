from game_message import *
from actions import *
import random


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, gameMsg: GameMessage):
        self.gameMsg = gameMsg

        ourTeamId = gameMsg.teamId
        otherTeamIds = [
            team for team in gameMsg.teams if team != gameMsg.teamId]
        actions = list()

        curTeam = 0

        if gameMsg.teamInfos[ourTeamId].money >= 200:
            buildAction: BuildAction = self.randomTowerPlacement()

            actions.append(buildAction)
            # pathPos: Position = gameMsg.map.paths[0].tiles[curIndex]
            # neighboursPositions = self.getNeighbours(pathPos, 1)
            # posIndex = random.randint(0, len(neighboursPositions) - 1)
            # towerPos = neighboursPositions[posIndex]
        else:
            actions.append(self.optimisationMoneyGagner()[0], otherTeamIds[curTeam % len(otherTeamIds)])
            actions.append(SendReinforcementsAction(
                EnemyType.LVL1, otherTeamIds[curTeam % len(otherTeamIds)]))
            curTeam += 1

        return actions

    def randomTowerPlacement(self) -> BuildAction:
        randX = random.randint(0, self.gameMsg.map.width - 1)
        randY = random.randint(0, self.gameMsg.map.height - 1)

        while not self.isCellEmpty(self.gameMsg.teamId, Position(randX, randY)):
            randX = random.randint(0, self.gameMsg.map.width - 1)
            randY = random.randint(0, self.gameMsg.map.height - 1)

        towerPos = Position(randX, randY)
        return BuildAction(TowerType.SPEAR_SHOOTER, towerPos)

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

                neighbours.append(Position(checkX, checkY))

        return neighbours

    def isCellOutOfBound(self, pos: Position):
        if pos.x >= self.gameMsg.map.width or pos.x < 0:
            return False
        if pos.y >= self.gameMsg.map.height or pos.y < 0:
            return False

        return True

    def isCellEmpty(self, teamId, pos: Position):
        if self.isCellOutOfBound(pos):
            return False

        cell = self.gameMsg.playAreas[teamId].grid[pos.x][pos.y]

        return len(cell.enemies) == 0 and len(cell.towers) == 0 and len(cell.paths) == 0

    
    def optimisationMoneyGagner(self):
        max = (EnemyType.LVL1, 0.1)
        for value in self.gameMsg.shop.reinforcements.keys():
            dictValues = self.gameMsg.shop.reinforcements[value]
            nb = dictValues.count
            rythme = dictValues.delayPerSpawnInTicks

            #secondeParEnvoi = nb/rythme
            secondePourEnvoyer = nb * rythme

            salaireAugmentation = dictValues.payoutBonus

            dollarParSeconde = salaireAugmentation/secondePourEnvoyer
            tuple(value, dollarParSeconde)
            
            if (max[1] < dollarParSeconde):
                max =tuple(value,dollarParSeconde)
        
        return max

    def OptimisationMoneyWin(self):
        max = (EnemyType.LVL1, 0.1)
        for value in self.gameMsg.shop.reinforcements.keys():
            dictValues = self.gameMsg.shop.reinforcements[value]

            salaireAugmentation = dictValues.payoutBonus
            salaireCount = dictValues.price
            ratioArgentCoutArgentWin = salaireCount/salaireAugmentation
            tuple(value, ratioArgentCoutArgentWin)
            
            if (max[1] < ratioArgentCoutArgentWin):
                max =tuple(value,ratioArgentCoutArgentWin)
        
        return max
