import numpy as np
import time
import copy
import sys
import os

from typing import *


WIDTH, HEIGHT = 15, 15

# BLACK = 1
# WHITE = -1
# EMPTY = 0
BLACK_ = 0
WHITE_ = 1
OUT = -2

BLACK_CHR = 'X'
WHITE_CHR = 'O'
EMPTY_CHR = '.'

RULE_GOMOKU = 1
RULE_RENJU = 2

GUI = 1
HEADLESS = 2

processes = 4


# class MoveProbPair:
#     def __init__(self, move: int, prob):
#         self.move = move
#         self.prob = prob


def move_int2xy(move_int: int) -> Tuple[int, int]:
    return move_int // WIDTH, move_int % WIDTH

def move_xy2int(x: int, y: int) -> int:
    return x * WIDTH + y

def move_int2cord(move_int):
    _x, _y = move_int2xy(move_int)
    return chr(_x + 97) + str(_y + 1)

def vector(*args, dtype=None):
    if dtype is None:
        return np.array(args)
    return np.array(args, dtype=dtype)

directions = vector(
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
)

