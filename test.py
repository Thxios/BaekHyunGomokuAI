import tensorflow as tf
import numpy as np
import time

from Network.Runner import ValueRunner, RolloutPolicyRunner, TreePolicyRunner



def board_to_input(b):
    _board = np.zeros((15, 15, 2))

    for x in range(15):
        for y in range(15):
            if b[x, y] == 1:
                _board[x, y, 0] = 1
            elif b[x, y] == 2:
                _board[x, y, 1] = 1

    return _board.reshape((1, 15, 15, 2))



if __name__ == '__main__':

    board = np.array([  # 1: Black 2: White
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0],  #
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])                        #

    n_stone = np.sum(board > 0)
    print(n_stone)

    print(board.shape)

    feed = board_to_input(board)

    st = time.time() * 1000
    v_predict = ValueRunner(feed)
    et = time.time() * 1000
    print(et - st, 'ms')
    print('%.3f%%' % (v_predict * 100))

    policy_feed = feed[:, :, :, (0, 1) if n_stone % 2 else (1, 0)]

    st = time.time() * 1000
    r_predict = RolloutPolicyRunner(policy_feed)
    et = time.time() * 1000
    print(et - st, 'ms')
    # print(r_predict.shape)
    print(np.array(np.round(r_predict.reshape((15, 15)) * 1000), dtype=np.int))

    st = time.time() * 1000
    t_predict = TreePolicyRunner(policy_feed)
    et = time.time() * 1000
    print(et - st, 'ms')
    print(np.array(np.round(t_predict.reshape((15, 15)) * 1000), dtype=np.int))



