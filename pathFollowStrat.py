import random
from typing import List, Dict

from strategy import *
from customMsg import *
from actions import *
from common import *


class PathFollowStrat(Strategy):
    def __init__(self):
        self.curTileIndex = 0

    def execute(self, gameMsg: GameMessage):
        actions = list()

        position: Position = gameMsg.map.paths[0].tiles[self.curTileIndex]
        neighbours = getNeighbours(gameMsg, position)

        if len(neighbours) > 0:
            actions.append(BuildAction(TowerType.SPEAR_SHOOTER, neighbours[0]))

        self.curTileIndex += 1

        return actions
