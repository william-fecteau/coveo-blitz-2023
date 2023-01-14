from game_message import *
from actions import *
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

        if self.gameMsg.teamInfos[self.gameMsg.teamId].money >= 200:
            randX = random.randint(0, self.gameMsg.map.width - 1)
            randY = random.randint(0, self.gameMsg.map.height - 1)

            towerPos = Position(randX, randY)

            actions.append(BuildAction(TowerType.SPEAR_SHOOTER, towerPos))
        else:
            if self.gameMsg.teamInfos[self.gameMsg.teamId].money >= 10:
                value = self.optimisationMoneyGagnerParSeconde()
                actions.append(SendReinforcementsAction(value[0], other_team_ids[0]))

        return actions

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
            tuple(value, ratioArgentCoutArgentWin)

            if (max[1] < ratioArgentCoutArgentWin):
                max = tuple(value, ratioArgentCoutArgentWin)

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
