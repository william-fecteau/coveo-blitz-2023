from __future__ import annotations

from dataclasses import dataclass
from game_message import *
from typing import List, Dict
from enum import Enum, unique
from cattrs.gen import make_dict_structure_fn, override
import cattrs


@dataclass
class Neighbour:
    position: Position
    tile: Tile
