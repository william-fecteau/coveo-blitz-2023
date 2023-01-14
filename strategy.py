from typing import List, Dict

from game_message import *
from customMsg import *
from actions import *
from strategy import *
from actions import *
from common import *


class Strategy:
    def execute(self, gameMsg: GameMessage):
        ourTeamId = gameMsg.teamId
        otherTeamIds = [
            team for team in gameMsg.teams if team != gameMsg.teamId]

        actions = list()
        return actions
