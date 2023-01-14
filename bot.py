from strat1 import *
from game_message import *


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, gameMsg: GameMessage):
        self.gameMsg = gameMsg

        strat = Strategy1()

        return strat.execute(gameMsg)

    def optimisationMoneyGagner(self):
        max = (EnemyType.LVL1, 0.1)
        for value in self.gameMsg.shop.reinforcements.keys():
            dictValues = self.gameMsg.shop.reinforcements[value]
            nb = dictValues.count
            rythme = dictValues.delayPerSpawnInTicks

            # secondeParEnvoi = nb/rythme
            secondePourEnvoyer = nb * rythme

            salaireAugmentation = dictValues.payoutBonus

            dollarParSeconde = salaireAugmentation/secondePourEnvoyer
            tuple(value, dollarParSeconde)

            if (max[1] < dollarParSeconde):
                max = tuple(value, dollarParSeconde)

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
                max = tuple(value, ratioArgentCoutArgentWin)

        return max
