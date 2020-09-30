from common import *


class TreeNode:
    # weight_c = np.sqrt(2)
    c_puct = 4

    def __init__(self, parent, prior_prob, depth=0):
        self.parent = parent
        self.probability = prior_prob
        self.depth = depth

        self.visit: int = 0
        self.sqrt_visit = 0.
        self.Q = 0
        self.U = 0

        self.children: Dict[int, TreeNode] = {}

    def __del__(self):
        self.children.clear()

    def leave_one_child(self, move: int):
        child_to_return = self.children[move]
        # self.children.clear()
        print(' selected action : ' + move_int2cord(move))
        print(' visit: %d   probability: %.3f%%   Q: %.4f\n' %
              (child_to_return.visit, child_to_return.probability * 100, child_to_return.Q))
        # print(child_to_return.visit, child_to_return.Q, child_to_return.probability * 100, ' ')
        return child_to_return

    def expand(self, policies: List[Tuple[int, float]]):
        # print(self, 'expand')
        # print(self, self.depth, 'expand')
        for policy in policies:
            # if policy[0] not in self.children:
            self.children[policy[0]] = TreeNode(self, policy[1], self.depth + 1)

    def backpropagate(self, bp_value):
        self.update(bp_value)
        if not self.is_root():
            self.parent.backpropagate(-bp_value)

    def update(self, bp_value):
        self.visit += 1
        self.sqrt_visit = np.sqrt(self.visit)
        self.Q += (bp_value - self.Q) / self.visit

    def p_uct(self) -> float:
        # self.U = (self.probability + 0.01) * np.sqrt(self.parent.visit) / (self.visit + 1)
        self.U = self.probability * self.parent.sqrt_visit / (self.visit + 1)
        Q = min(self.visit / 10, 1) * self.Q
        # return self.Q + self.W_c * self.U
        return Q + self.c_puct * self.U

    def select(self):
        return max(self.children.items(), key=lambda pair: pair[1].p_uct())

    def is_root(self) -> bool:
        return self.parent is None

    def is_leaf(self) -> bool:
        return len(self.children) == 0

