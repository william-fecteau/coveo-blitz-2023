from game_message import *
from actions import *
import bot 


def optimisationMoneyGagnerParSeconde(gameMsg):
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
def OptimisationMoneyRentabiliter(gameMsg):
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