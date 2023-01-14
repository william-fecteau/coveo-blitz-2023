from game_message import *
from actions import *
from common import *
from dataJellyFish import *
import random


class Bot:
    def __init__(self):
        self.tileIndexes = None
        self.pathIndex = 0

    def get_next_move(self, gameMsg: GameMessage):
        self.gameMsg = gameMsg

        return self.followPathStrat()

    def followPathStrat(self):
        actions = list()

        # TODO: MAKE BETTER ECONOMY CHOICE
        if self.gameMsg.teamInfos[self.gameMsg.teamId].money >= 10:
            other_team_ids = [
                team for team in self.gameMsg.teams if team != self.gameMsg.teamId]
            value = self.optimisationMoneyGagnerParSeconde()

            actions.append(SendReinforcementsAction(
                value[0], other_team_ids[0]))

        if self.gameMsg.teamInfos[self.gameMsg.teamId].money <= 260:
            return actions

        nbPaths = len(self.gameMsg.map.paths)
        if self.tileIndexes is None:
            self.tileIndexes = [0 for _ in range(nbPaths)]

        self.pathIndex = self.pathIndex % nbPaths

        if self.tileIndexes[self.pathIndex] >= len(self.gameMsg.map.paths[self.pathIndex].tiles):
            self.tileIndexes[self.pathIndex] = 0

        pathPos = self.gameMsg.map.paths[self.pathIndex].tiles[self.tileIndexes[self.pathIndex]]
        neighbours: list[Neighbour] = getNeighbours(self.gameMsg, pathPos)

        foundPlace = False
        for neighbour in neighbours:
            if isTileEmpty(neighbour.tile):
                actions.append(BuildAction(
                    TowerType.SPEAR_SHOOTER, neighbour.position))
                foundPlace = True
                break

        self.tileIndexes[self.pathIndex] += 5

        if foundPlace:
            self.pathIndex += 1

        return actions

    def randomPlacementStrat(self):
        actions = list()
        other_team_ids = [
            team for team in self.gameMsg.teams if team != self.gameMsg.teamId]

        roundNumber = self.gameMsg.round
        t = getNeighbours(self.gameMsg, Position(0, 0))
        if self.gameMsg.teamInfos[self.gameMsg.teamId].money >= 10:
            value = self.optimisationMoneyGagnerParSeconde()
            actions.append(SendReinforcementsAction(
                value[0], other_team_ids[0]))

        if self.gameMsg.teamInfos[self.gameMsg.teamId].money >= 250:
            towerPos = positionRandom()

            actions.append(BuildAction(TowerType.SPEAR_SHOOTER, towerPos))
        return actions

    def attackAfterRound10(self) -> BuildAction:
        actions = list()
        other_team_ids = [
            team for team in self.gameMsg.teams if team != self.gameMsg.teamId]
        # prio send attack
        bestDPS = self.OptimisationDmgTime()
        if self.gameMsg.teamInfos[self.gameMsg.teamId].money >= 100:
            actions.append(SendReinforcementsAction(
                bestDPS[0], other_team_ids[0]))
        if self.gameMsg.teamInfos[self.gameMsg.teamId].money >= 1000:
            towerPos = positionRandom()

            actions.append(BuildAction(TowerType.SPEAR_SHOOTER, towerPos))

    def optimisationMoneyGagnerParSeconde(self) -> tuple[EnemyType, float]:
        max = (EnemyType.LVL1, 0.1)
        for value in self.gameMsg.shop.reinforcements.keys():
            dictValues = self.gameMsg.shop.reinforcements[value]
            nb = dictValues.count
            rythme = dictValues.delayPerSpawnInTicks

            # secondeParEnvoi = nb/rythme
            secondePourEnvoyer = nb * rythme

            salaireAugmentation = dictValues.payoutBonus

            dollarParSeconde = salaireAugmentation/secondePourEnvoyer

            if (max[1] < dollarParSeconde):
                max = (value, dollarParSeconde)

        return max

    def OptimisationMoneyRentabiliter(self):
        max = (EnemyType.LVL1, 0.1)
        for value in self.gameMsg.shop.reinforcements.keys():
            dictValues = self.gameMsg.shop.reinforcements[value]

            salaireAugmentation = dictValues.payoutBonus
            salaireCount = dictValues.price
            ratioArgentCoutArgentWin = salaireCount/salaireAugmentation
            (value, ratioArgentCoutArgentWin)

            if (max[1] < ratioArgentCoutArgentWin):
                max = (value, ratioArgentCoutArgentWin)

        return max

    def OptimisationDmgMoney(self):
        max = (EnemyType.LVL1, 0.1)
        lvl = 0
        for value in self.gameMsg.shop.reinforcements.keys():
            lvl += 1
            dictValues = self.gameMsg.shop.reinforcements[value]

            maxDamage = EnnemiStats["ennemi"][f'lvl{lvl}']['maxHP'] * \
                dictValues.count
            dmgPerMoney = maxDamage / dictValues.price

            if (max[1] < dmgPerMoney):
                max = tuple(value, dmgPerMoney)

        return max

    def OptimisationDmgTime(self):
        max = (EnemyType.LVL1, 0.1)
        lvl = 0
        for value in self.gameMsg.shop.reinforcements.keys():
            lvl += 1
            dictValues = self.gameMsg.shop.reinforcements[value]

            maxDamage = EnnemiStats["ennemi"][f'lvl{lvl}']['maxHP'] * \
                dictValues.count
            dmgPerTime = maxDamage / dictValues.delayPerSpawnInTicks

            if (max[1] < dmgPerTime):
                max = tuple(value, dmgPerTime)

        return max
