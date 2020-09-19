from common import *

from Gomoku.Agent import _Agent
from MCTS.Tree import MonteCarloTree
from Gomoku.Board import Board
from MCTS.NetworkFunction import expand_policy_network, rollout_policy_network



class DeepAgentMCTS(_Agent):
    def __init__(self, compute_budget: int):
        self.mct = MonteCarloTree(
            compute_budget=compute_budget,
            expand_bound=max(compute_budget // 500, 5),
            rollout_limit=100,
            use_network=True
        )

    def get_action(self, board: Board) -> int:
        self.mct.update_with_move(board.last_move)

        next_move = self.mct.get_move(board)
        self.mct.update_with_move(next_move)

        return next_move


class PureAgentMCTS(_Agent):
    def __init__(self, compute_budget):
        self.mct = MonteCarloTree(
            compute_budget=compute_budget,
            expand_bound=max(compute_budget // 500, 5),
            rollout_limit=200,
            use_network=False
        )

    def get_action(self, board: Board) -> int:
        self.mct.update_with_move(board.last_move)

        next_move = self.mct.get_move(board)
        self.mct.update_with_move(next_move)

        return next_move
