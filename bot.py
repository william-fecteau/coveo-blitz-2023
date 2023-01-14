from game_message import *
from actions import *
from common import *
from dataJellyFish import *
import random


class Bot:
    def __init__(self):
        self.tileIndexes = None
        self.pathIndex = 0
        self.EcoBase = 225
        self.EcoScaling = 25
        self.spearLoop = 0
        self.step = 5
        self.spearmanStart = 6

    def getAliveTeams(self):
        other_team_ids = [
            team for team in self.gameMsg.teams if team != self.gameMsg.teamId]

        aliveTeams = []
        for teamId in other_team_ids:
            if self.gameMsg.teamInfos[teamId].isAlive:
                aliveTeams.append(teamId)

        return aliveTeams

    def get_next_move(self, gameMsg: GameMessage):
        self.gameMsg = gameMsg

        roundNumber = self.gameMsg.round
        if roundNumber >= 2 and self.estCeQuonSeFaitCasserLesFesses() and len(self.getAliveTeams()) > 2:
            self.aggresiveBuild()
        if roundNumber > 15:
            return self.attackAfterRound10()

        return self.followPathStrat()

    def calculEco(self):
        roundNumber = self.gameMsg.round
        return self.EcoBase + roundNumber*25

    def estCeQuonSeFaitCasserLesFesses(self):
        other_team_ids = [
            team for team in self.gameMsg.teams if team != self.gameMsg.teamId]

        enemies = []
        for teamId in other_team_ids:
            enemies.append(len(self.gameMsg.playAreas[teamId].enemies))

        maxEnemy = max(enemies)
        ourEnemy = len(self.gameMsg.playAreas[self.gameMsg.teamId].enemies)

        if ourEnemy == 0:
            ourEnemy = 1

        ratio = float(maxEnemy)/float(ourEnemy)

        return ratio > 1.2

    def placeSpearman(self, actions):
        nbPaths = len(self.gameMsg.map.paths)
        if self.tileIndexes is None:
            self.tileIndexes = [self.spearmanStart for _ in range(nbPaths)]

        self.pathIndex = self.pathIndex % nbPaths

        if self.tileIndexes[self.pathIndex] >= len(self.gameMsg.map.paths[self.pathIndex].tiles):
            self.spearLoop += 1

            if self.spearLoop == 1:
                self.spearmanStart = 0
                self.step = 2
            if self.spearLoop == 2:
                self.step = 1

            self.tileIndexes[self.pathIndex] = self.spearmanStart

        pathPos = self.gameMsg.map.paths[self.pathIndex].tiles[self.tileIndexes[self.pathIndex]]
        neighbours: list[Neighbour] = getNeighbours(self.gameMsg, pathPos)

        foundPlace = False
        for neighbour in neighbours:
            if isTileEmpty(neighbour.tile):
                actions.append(BuildAction(
                    TowerType.SPEAR_SHOOTER, neighbour.position))
                foundPlace = True
                break

        self.tileIndexes[self.pathIndex] += self.step

        if foundPlace:
            self.pathIndex += 1

    def placeSpike(self, actions):
        posAndCount = self.bestPositionSpike()

        spikeCount = countTowerType(self.gameMsg, TowerType.SPIKE_SHOOTER)
        spearmanCount = countTowerType(self.gameMsg, TowerType.SPEAR_SHOOTER)

        if spikeCount == 0:
            spikeCount = 1

        ratio = float(spearmanCount)/float(spikeCount)

        if posAndCount[1] > 6 and ratio < 3:
            actions.append(BuildAction(
                TowerType.SPIKE_SHOOTER, posAndCount[0]))
            return

        # spearmanCount = countTowerType(self.gameMsg, TowerType.SPEAR_SHOOTER)
        # if spearmanCount > 7:
        #     actions.append(BuildAction(
        #         TowerType.SPIKE_SHOOTER, posAndCount[0]))

    def followPathStrat(self):
        actions = list()

        roundNumber = self.gameMsg.round

        # Economy
        if self.gameMsg.teamInfos[self.gameMsg.teamId].money >= 15:
            if len(self.gameMsg.teamInfos[self.gameMsg.teamId].sentReinforcements) < 8:
                value = self.optimisationMoneyGagnerParSeconde()

                targettedTeam = self.selectAliveTeam()
                if len(self.gameMsg.playAreas[targettedTeam].enemyReinforcementsQueue) < 8:
                    actions.append(SendReinforcementsAction(
                        value[0], targettedTeam))

        if self.gameMsg.teamInfos[self.gameMsg.teamId].money <= self.OptimisationArgentPourEco():
            return actions

        self.placeSpike(actions)
        self.placeSpearman(actions)

        return actions

    def aggresiveBuild(self):
        actions = list()

        print("Aggressive build")
        roundNumber = self.gameMsg.round

        self.placeSpike(actions)
        self.placeSpearman(actions)

        return actions

    def selectAliveTeam(self):
        aliveTeams = self.getAliveTeams()

        return random.choice(aliveTeams)

    def attackAfterRound10(self) -> BuildAction:
        actions = list()

        # prio send attack
        bestDPS = self.OptimisationDmgTime()
        if self.gameMsg.teamInfos[self.gameMsg.teamId].money >= 100:
            targettedTeam = self.selectAliveTeam()
            if len(self.gameMsg.playAreas[targettedTeam].enemyReinforcementsQueue) < 8:
                actions.append(SendReinforcementsAction(
                    bestDPS[0], targettedTeam))
        if self.gameMsg.teamInfos[self.gameMsg.teamId].money >= 1000:
            towerPos = positionRandom(self.gameMsg)

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

    def bestPositionSpike(self):
        goodPosSet = set()
        for path in self.gameMsg.map.paths:
            tilesList = path.tiles
            tilesList.pop(-1)

            for pos in tilesList:
                posList: List[Neighbour] = getNeighbours(self.gameMsg, pos)

                for i in posList:
                    if not isTileEmpty(i.tile):
                        continue

                    countSpike = 0
                    neighbourList = getNeighbours(self.gameMsg, i.position)
                    for j in neighbourList:
                        if j.tile is None:
                            continue

                        if len(j.tile.paths) != 0:
                            countSpike += 1
                    goodPosSet.add((i.position, countSpike))
        maxTuple = (Position(0, 0), 0)
        for i in goodPosSet:
            if i[1] > maxTuple[1]:
                maxTuple = i
        print(maxTuple[1])
        return maxTuple

    def OptimisationArgentPourEco(self):
        nbPaths = len(self.gameMsg.map.paths)
        nombreRound = self.gameMsg.round
        if (nbPaths == 1):
            self.EcoBase = 250
            self.EcoScaling = 45
        if (nbPaths == 2):
            self.EcoBase = 240
            self.EcoScaling = 35
        if (nbPaths == 4):
            self.EcoBase = 225
            self.EcoScaling = 25
        if nbPaths == 5:
            self.EcoBase = 225
            self.EcoScaling = 25
        if nbPaths == 6:
            self.EcoBase = 215
            self.EcoScaling = 25
        return self.EcoBase + nombreRound*self.EcoScaling
