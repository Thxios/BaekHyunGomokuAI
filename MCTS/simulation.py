from common import *

from Gomoku.Board import Board
from MCTS.policy import rollout_policy_network, rollout_policy_random

from Network.Runner import ValueRunner


def simulate_network(board: Board, limit=100, q_confidence=0.5):
    random_bound = 4
    net_run_time = 0.
    start_time = time.time() * 1000

    is_end, winner = False, None

    for i in range(limit):
        is_end, winner = board.check_winner()
        if is_end:
            # print(i, 'end')
            break

        must = board.check_must()
        if must is not None:
            if not board.play(must):
                raise ValueError('Must Error')
            continue

        t1 = time.time() * 1000
        action_prob = rollout_policy_network(board)
        # action_prob = policy(board)
        t2 = time.time() * 1000
        net_run_time += t2 - t1

        if i < random_bound:
            next_action = np.random.choice(15 * 15, 1, p=action_prob)[0]

            while not board.play(next_action):
                next_action = np.random.choice(15 * 15, 1, p=action_prob)[0]

        else:
            next_action = max(board.available, key=lambda move: action_prob[move])
            board.play(next_action)

    end_time = time.time() * 1000

    # print('%.5fms  %.5fms  %.5f%%' % (end_time - start_time, net_run_time, net_run_time * 100 / (end_time - start_time)))
    if is_end:
        if winner is not None:
            return winner
    value_network_Q = ValueRunner(board.get_board_array())
    if board.current_player == BLACK_:  # array shape (white, black)
        value_network_Q = 1 - value_network_Q  # change to black side
    return q_confidence * (value_network_Q - 0.5) + 0.5


def simulate_random(board: Board, limit=200):
    net_run_time = 0.
    start_time = time.time() * 1000

    is_end, winner = False, None

    for i in range(limit):
        is_end, winner = board.check_winner()
        if is_end:
            # print(i, 'end')
            break

        must = board.check_must()
        if must is not None:
            # if board.play(must):
            #     continue
            if not board.play(must):
                raise ValueError('Must Error')
            # board.show()
            continue

        t1 = time.time() * 1000
        action_prob = rollout_policy_random(board)
        # action_prob = policy(board)
        t2 = time.time() * 1000
        net_run_time += t2 - t1

        next_action = np.argmax(action_prob)

        while not board.play(next_action):
            next_action = np.argmax(action_prob)

    end_time = time.time() * 1000

    # print('%.5fms  %.5fms  %.5f%%' % (end_time - start_time, net_run_time, net_run_time * 100 / (end_time - start_time)))
    if is_end:
        if winner is not None:
            return winner

    return 0.5


