from game_message import *
from actions import *
from common import *
from dataJellyFish import *
import random


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, gameMsg: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        self.gameMsg = gameMsg

        return self.randomPlacementStrat()

    def randomPlacementStrat(self) -> BuildAction:
        actions = list()
        other_team_ids = [
            team for team in self.gameMsg.teams if team != self.gameMsg.teamId]

        t = getNeighbours(self.gameMsg, Position(0, 0))
        if self.gameMsg.teamInfos[self.gameMsg.teamId].money >= 10:
            value = self.optimisationMoneyGagnerParSeconde()
            actions.append(SendReinforcementsAction(
                value[0], other_team_ids[0]))


        if self.gameMsg.teamInfos[self.gameMsg.teamId].money >= 250:
            randX = random.randint(0, self.gameMsg.map.width - 1)
            randY = random.randint(0, self.gameMsg.map.height - 1)

            towerPos = Position(randX, randY)

            actions.append(BuildAction(TowerType.SPEAR_SHOOTER, towerPos))
        return actions

    def attackAfterRound10(self) -> BuildAction:
        actions = list()
        other_team_ids = [
            team for team in self.gameMsg.teams if team != self.gameMsg.teamId]
        #prio send attack
        if self.gameMsg.teamInfos[self.gameMsg.teamId].money <= 100:
            actions.append(SendReinforcementsAction(self.OptimisationMoneyRentabiliter()[0], other_team_ids[0]))

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
            lvl +=1
            dictValues = self.gameMsg.shop.reinforcements[value]

            maxDamage = EnnemiStats["ennemi"][f'lvl{lvl}']['maxHP'] * dictValues.count
            dmgPerMoney = maxDamage / dictValues.price            

            if (max[1] < dmgPerMoney):
                max = tuple(value, dmgPerMoney)

        return max

    def OptimisationDmgTime(self):
        max = (EnemyType.LVL1, 0.1)
        lvl = 0
        for value in self.gameMsg.shop.reinforcements.keys():
            lvl +=1
            dictValues = self.gameMsg.shop.reinforcements[value]

            maxDamage = EnnemiStats["ennemi"][f'lvl{lvl}']['maxHP'] * dictValues.count
            dmgPerTime = maxDamage / dictValues.delayPerSpawnInTicks            

            if (max[1] < dmgPerTime):
                max = tuple(value, dmgPerTime)

        return max

    def bestPositionSpike(self):
        
        for path in self.gameMsg.map.paths:
            for pos in path.tiles:
                posList = getNeighbours(pos)
                goodPosSet = set() 
                for i in posList:
                    count = 0
                    neighbourList = getNeighbours(i.position)
                    for j in neighbourList:
                        if len(j.tile.paths) != 0:
                            count += 1
                    goodPosSet.add((i.position, count))
        
        max = (0,0)
        for i in goodPosSet:
            if i[1] > max[1]:
                max = i
        if max[1] >=4:
            return max  
        return None

