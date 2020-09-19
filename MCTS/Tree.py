from common import *
from tqdm import tqdm

from Gomoku.Board import Board

from MCTS.Node import TreeNode
from MCTS.NetworkFunction import expand_policy_network, expand_pocliy_random
from MCTS.simulation import simulate_network, simulate_random
from MCTS.log import Log

class MonteCarloTree:
    value_confidence = 0.5

    def __init__(
            self,
            compute_budget: int,
            expand_bound: int,
            rollout_limit: int,
            use_network: bool,
    ):
        self.compute_budget = compute_budget
        self.expand_bound = expand_bound
        self.rollout_limit = rollout_limit
        self.network = use_network

        self.root = TreeNode(None, 1.)

    def rollout_simulation(self, board: Board):
        current_turn = board.current_player
        if self.network:
            simulation_result = simulate_network(board, self.rollout_limit, self.value_confidence)
        else:
            simulation_result = simulate_random(board, self.rollout_limit)

        if current_turn == BLACK_:
            return 2 * simulation_result - 1
        else:
            return -2 * simulation_result + 1

    def playout(self, state: Board):
        node = self.root
        start_depth = self.root.depth

        while 1:
            if node.is_leaf():
                # if node.depth < 5 or node.depth < 2 + start_depth or node.visit >= self.expand_bound:
                if (node.depth < start_depth + 5 and node.visit > (node.depth - start_depth) * 2) \
                        or node.visit >= self.expand_bound:
                    if self.network:
                        policy = expand_policy_network(state)
                    else:
                        policy = expand_pocliy_random(state)
                    node.expand(policy)
                else:
                    break
            action, node = node.select()
            state.play(action)

            is_end, _ = state.check_winner()

            if is_end:
                break

        # bp_value = self.evaluate_rollout(state)
        # bp_value = self.evaluate_rollout_v2(state)
        # for _ in range(self.expand_bound):
        #     bp_value = self.rollout_simulation(state.copy())
        #     node.backpropagate(bp_value)

        bp_value = self.rollout_simulation(state)
        node.backpropagate(bp_value)

    def get_move(self, state: Board):
        if state.is_empty():
            return move_xy2int(WIDTH // 2, HEIGHT // 2)

        time.sleep(0.1)
        start_time = time.time()

        if len(state.moved) == 1 or len(state.moved) == 2:
            it = self.compute_budget // 2
        else:
            it = self.compute_budget

        for i in tqdm(range(it)):
            board_to_search = state.copy()
            self.playout(board_to_search)

        end_time = time.time()
        children = self.root.children.items()

        Log.silent_log('%d playouts in %.3f second' % (self.compute_budget, end_time - start_time))
        Log.silent_log('average : %.3f ms\n' % ((end_time - start_time) / self.compute_budget * 1000))
        Log.silent_log('most visited node:')
        Log.silent_log('|  ' + 'action'.ljust(8, ' ')
                       + '|  ' + 'visit'.ljust(8, ' ') + '|  ' + 'probability'.ljust(13, ' ') + '|  ' + '   Q      |')
        for action, c in sorted(children, key=lambda child: child[1].visit, reverse=True)[:5]:
            if c.visit == 0 and c.probability < 0.01:
                continue
            # print(move_int2xy(action),
            #       '  \tvisit: {0}  \teval:  {1:.5f}  \tQ: {2:.5f}  \tprob: {3:.2f}%'.format(
            #           c.visit, c.evaluate(), c.Q, c.probability * 100))
            # print('%s\t\t%d   \t   %.2f%%   \t%.4f' % (move_int2xy(action), c.visit, c.probability * 100, c.Q))
            Log.silent_log('|  ' + ' ' + str(move_int2cord(action)).ljust(7, ' ') + '|  ' + \
                           (' %d' % c.visit).ljust(8, ' ') + '|  ' + \
                           (' %.3f%%' % (c.probability * 100)).ljust(13, ' ') + '|  ' + \
                           ('%.4f' % c.Q).rjust(7, ' ') + '   |')
        most_visited_move = max(children, key=lambda child: child[1].visit)[0]
        # print('mean:', sum(t) / len(t), 'ms')
        # print('acc:', sum(check) / len(check) * 100, '%')
        # print('q:', sum(q_log) / len(q_log))

        return most_visited_move

    def update_with_move(self, last_move: int):
        if last_move == -1:
            return

        if last_move in self.root.children:
            next_root = self.root.leave_one_child(last_move)
            self.root = next_root
        else:
            self.root = TreeNode(None, 1.)
