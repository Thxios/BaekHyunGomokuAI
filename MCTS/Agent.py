from common import *

from Gomoku.Agent import _Agent
from MCTS.Tree import MonteCarloTree
from Gomoku.Board import Board
from MCTS.policy import expand_policy_network, rollout_policy_network



class DeepMCTSAgent(_Agent):
    use_mcts = True
    use_network = True

    def __init__(self, compute_budget: int):
        self.compute_budget = compute_budget
        self.mct = MonteCarloTree(
            compute_budget=compute_budget,
            expand_threshold=6,
            rollout_limit=100,
            use_network=True
        )

    def get_action(self, board: Board) -> int:
        self.mct.update_with_move(board.last_move)

        next_move = self.mct.get_move(board)
        self.mct.update_with_move(next_move)

        return next_move


class PureMCTSAgent(_Agent):
    use_mcts = True

    def __init__(self, compute_budget):
        self.compute_budget = compute_budget
        self.mct = MonteCarloTree(
            compute_budget=compute_budget,
            expand_threshold=1,
            rollout_limit=200,
            use_network=False
        )

    def get_action(self, board: Board) -> int:
        self.mct.update_with_move(board.last_move)

        next_move = self.mct.get_move(board)
        self.mct.update_with_move(next_move)

        return next_move
