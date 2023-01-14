import random
from typing import List, Dict

from strategy import *
from customMsg import *
from actions import *
from common import *
from OptimisationEco import *


class Strategy1(Strategy):
    def execute(self, gameMsg: GameMessage):
        actions = list()

        randX = random.randint(0, gameMsg.map.width - 1)
        randY = random.randint(0, gameMsg.map.height - 1)

        while not isCellEmpty(gameMsg.teamId, Position(randX, randY)):
            randX = random.randint(0, gameMsg.map.width - 1)
            randY = random.randint(0, gameMsg.map.height - 1)

        towerPos = Position(randX, randY)

        otherTeamIds = [
            team for team in gameMsg.teams if team != gameMsg.teamId]

        actions.append(BuildAction(TowerType.SPEAR_SHOOTER, towerPos))
        actions.append(SendReinforcementsAction(EnemyType.LVL1, otherTeamIds[0]))
        actions.append(SendReinforcementsAction(optimisationMoneyGagnerParSeconde(gameMsg)[0], otherTeamIds[0]))
        return actions
