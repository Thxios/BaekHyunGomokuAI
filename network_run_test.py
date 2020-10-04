from common import *


from Gomoku.Board import Board
from Network.Runner import TreePolicyRunner, RolloutPolicyRunner
from MCTS.policy import _convolve_board_available_narrow

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

mul = 1000

if __name__ == '__main__':
    b_arr = board_to_run.get_board_array()
    t1 = time.time() * 1000
    for _ in range(mul - 1):
        tree = TreePolicyRunner(b_arr)
    tree = TreePolicyRunner(b_arr)
    t2 = time.time() * 1000
    for _ in range(mul - 1):
        rollout = RolloutPolicyRunner(b_arr)
    rollout = RolloutPolicyRunner(b_arr)
    t3 = time.time() * 1000
    for _ in range(mul - 1):
        available = _convolve_board_available_narrow(b_arr)
    available = _convolve_board_available_narrow(b_arr).reshape((15, 15)) * np.ones((15, 15)) #- b_arr[:, :, 0] - b_arr[:, :, 1]
    cnt = available.sum()
    available = available / cnt
    t4 = time.time() * 1000

    tree = tree.reshape((15, 15)).T
    tree = np.array(np.round(tree * 100), dtype=np.int)
    rollout = rollout.reshape((15, 15)).T
    rollout = np.array(np.round(rollout * 100), dtype=np.int)
    available = np.array(np.round(available * 1000), dtype=np.int).T


    print('\n\ntree:')
    print(tree)
    print((t2 - t1) / mul, 'ms')
    print('\n\nrollout:')
    print(rollout)
    print((t3 - t2) / mul, 'ms')
    print('\n\n', available)
    print(available.sum())
    print((t4 - t3) / mul, 'ms')



