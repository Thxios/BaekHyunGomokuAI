from common import *

from Gomoku.Board import Board
from MCTS.simulation import simulate_network, simulate_random
from MCTS.policy import rollout_policy_network, rollout_policy_random


test = [
    [
        (7, 7),
        (7, 6),
        (8, 6),
        (9, 5),
        (8, 8),
        (7, 5),
        (6, 5),
        (6, 7),
    ],
    [
        (7, 7),
        (8, 6),
        (8, 7),
        (9, 7),
        (7, 5),
        (7, 6),
        (9, 6),
        (10, 5),
        (5, 5),
        (10, 6),
    ],
    [
        (7, 7),
        (8, 6),
        (7, 8),
        (7, 9),
        (8, 8),
        (6, 6),
        (6, 7),
        (5, 7),
        (5, 6),
        (8, 9),
        (7, 5),
        (7, 6),
        (9, 6),
        (6, 8),
        (8, 10),
        (8, 7),
    ],
    [
        (7, 7),
        (8, 7),
        (8, 6),
        (6, 6),
        (9, 5),
        (10, 4),
        (7, 8),
        (7, 9),
        (7, 5),
        (9, 4),
        (8, 5),
        (6, 5),
        (7, 4),
        (7, 6),
        (9, 8),
        (10, 8),
    ],
    [
        (7, 7),
        (8, 6),
        (7, 6),
        (7, 5),
        (9, 7),
        (8, 7),
        (8, 8),
        (7, 9),
        (9, 9),
        (7, 8),
    ],
    [
        (7, 7),
        (8, 6),
        (7, 6),
        (7, 5),
        (9, 7),
        (8, 7),
        (8, 8),
        (7, 9),
        (9, 9),
    ],
    [
        (7, 7),
        (6, 7),
        (6, 8),
        (8, 6),
        (8, 8),
        (7, 8),
        (8, 9),
        (9, 9),
        (8, 10),
        (8, 11),
        (7, 9),
        (5, 7),
        (6, 10),
        (5, 11),
        (7, 10),
        (5, 10),
        (6, 11),
        (5, 12),
        (5, 9),
        (6, 9),
        (8, 7),
        (4, 11),
        (3, 12),
        (3, 10),
    ],
    [
        (7, 7),
        (8, 7),
        (7, 8),
        (7, 6),
        (9, 8),
        (8, 8),
        (8, 9),
        (9, 10),
        (7, 10),
        (6, 11),
        (7, 9),
        (7, 11),
        (6, 9),
        (5, 9),
        (8, 11),
        (5, 8),
    ],
]

n_test = 7

board_to_run = Board()
for x, y in test[n_test]:
    board_to_run.play(move_xy2int(x, y))
board_to_run.show()


if __name__ == '__main__':
    res = []
    for i in range(10):
        _board = board_to_run.copy()
        # res.append(simulate_network(_board))
        res.append(simulate_random(_board))
        # _board.show()


    print(res)

