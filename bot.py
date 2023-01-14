from randomPlacementStrat import *
from pathFollowStrat import *
from game_message import *


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, gameMsg: GameMessage):
        self.gameMsg = gameMsg

        strat = PathFollowStrat()

        return strat.execute(gameMsg)
