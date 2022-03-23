from common import *
from Network.networks import create_rollout_policy_network, create_value_network, create_tree_policy_network, \
    create_rollout_policy_network_v2, create_tree_policy_network_v2


# print(__name__)


class _Runner:
    save: Dict[str, str]

    def __init__(self):
        self.model = None
        self._restored = False
        self.runtime = 0
        self.run_count = 0

    def reset_runtime(self):
        self.runtime = 0
        self.run_count = 0

    def __call__(self, x: np.ndarray):
        if not self._restored:
            raise ValueError('model not restored')

        start_time = time.time() * 1000

        input_data = x.reshape((1, 15, 15, 2))
        predict = self.model(input_data)

        end_time = time.time() * 1000
        self.runtime += end_time - start_time
        self.run_count += 1

        return predict

    def restore(self, tag):
        cp_path = self.save[tag]
        self.model.load_weights(cp_path)
        self._restored = True


class RolloutPolicyNetwork(_Runner):
    save = {
        # 'test1_128kernel': 'Network/save/rollout/test2/cp.ckpt',
        # 'colab_64_32': 'Network/colab/rollout/rollout_64_32/cp-010.ckpt',
        # 'colab_64_32_v2': 'Network/colab/rollout/rollout_64_32/cp-010.ckpt',
        # 'colab_64_32_32': 'Network/colab/rollout/64_32_32/cp-010.ckpt',
        # '64_32_32': 'model/rollout_64_32_32/cp-010.ckpt',
        'rollout_final': 'model/rollout/cp-005.ckpt',
    }

    def __init__(self):
        super().__init__()
        # self.model = create_rollout_policy_network()
        self.model = create_rollout_policy_network_v2()

    def __call__(self, x: np.ndarray):
        predict = super().__call__(x)
        return np.reshape(predict, (15 * 15,))


class TreePolicyNetwork(_Runner):
    save = {
        # '005_128': 'Network/save/tree/test1_128kernel/cp-005.ckpt',
        # '005_64': 'Network/save/tree/test2_64kernel/cp-005.ckpt',
        # 'colab_128': 'Network/colab/tree/tree_128/cp-005.ckpt',
        # 'colab_128_v2': 'Network/colab/tree/tree_128_v2/cp-005.ckpt',
        # 'colab_128_128_64x2': 'Network/colab/tree/128_128_64x2/cp-005.ckpt',
        # '128_v2': 'model/tree_128_128_128/cp-005.ckpt',
        'tree_final': 'model/tree/cp-005.ckpt',
    }

    def __init__(self):
        super().__init__()
        self.model = create_tree_policy_network()
        # self.model = create_tree_policy_network_v2()

    def __call__(self, x: np.ndarray):
        predict = super().__call__(x)
        return np.reshape(predict, (15 * 15,))


class ValueNetwork(_Runner):
    save = {
        # 'ccpc': 'Network/save/value/test1_ccpc/cp-005.ckpt',
        # 'swap1': 'Network/save/value/swap1/cp-005.ckpt',
        # 'swap': 'model/value_swap/cp-005.ckpt',
        'value_final': 'model/value/cp-005.ckpt',
    }

    def __init__(self):
        super().__init__()
        self.model = create_value_network()

    def __call__(self, x: np.ndarray):
        predict = super().__call__(x)
        return np.array(predict)[0, 0]



# print(__name__)

RolloutPolicyRunner = RolloutPolicyNetwork()
# RolloutPolicyRunner.restore('colab_64_32_32')
RolloutPolicyRunner.restore('rollout_final')
# print('RolloutPolicyRunner: ', id(RolloutPolicyRunner))

TreePolicyRunner = TreePolicyNetwork()
# TreePolicyRunner.restore('colab_128')
TreePolicyRunner.restore('tree_final')
# print('TreePolicyRunner: ', id(TreePolicyRunner))

ValueRunner = ValueNetwork()
# ValueRunner.restore('swap1')
ValueRunner.restore('value_final')
# print('ValueRunner: ', id(ValueRunner))


