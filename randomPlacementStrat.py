import random
from typing import List, Dict

from strategy import *
from customMsg import *
from actions import *
from common import *


class RandomPlacementStrat(Strategy):
    def execute(self, gameMsg: GameMessage):
        actions = list()

        randX = random.randint(0, gameMsg.map.width - 1)
        randY = random.randint(0, gameMsg.map.height - 1)

        while not isCellEmpty(gameMsg.teamId, Position(randX, randY)):
            randX = random.randint(0, gameMsg.map.width - 1)
            randY = random.randint(0, gameMsg.map.height - 1)

        towerPos = Position(randX, randY)

        actions.append(BuildAction(TowerType.SPEAR_SHOOTER, towerPos))

        return actions
