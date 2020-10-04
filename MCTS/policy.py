from common import *
import scipy.signal as sig

from Gomoku.Board import Board

from Network.Runner import RolloutPolicyRunner, TreePolicyRunner



__second_move_available = {
    move_xy2int(6, 6),
    move_xy2int(6, 7),
    move_xy2int(6, 8),
    move_xy2int(7, 6),
    move_xy2int(7, 8),
    move_xy2int(8, 6),
    move_xy2int(8, 7),
    move_xy2int(8, 8),
}

__available_kernel_wide = np.array([
    [1, 0, 0, 1, 0, 0, 1],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [1, 1, 1, -99, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [1, 0, 0, 1, 0, 0, 1],
])

__available_kernel_narrow = np.array([
    [1, 0, 1, 0, 1],
    [0, 1, 1, 1, 0],
    [1, 1, -99, 1, 1],
    [0, 1, 1, 1, 0],
    [1, 0, 1, 0, 1],
])



def _convolve_board_available_wide(board_array):
    convolved_1 = sig.convolve2d(board_array[:, :, 0], __available_kernel_wide, 'same')
    convolved_2 = sig.convolve2d(board_array[:, :, 1], __available_kernel_wide, 'same')
    return np.array(convolved_1 + convolved_2 > 0, dtype=np.int).reshape((15 * 15,))


def _convolve_board_available_narrow(board_array):
    convolved_1 = sig.convolve2d(board_array[:, :, 0], __available_kernel_narrow, 'same')
    convolved_2 = sig.convolve2d(board_array[:, :, 1], __available_kernel_narrow, 'same')
    return np.array(convolved_1 + convolved_2 > 0, dtype=np.int).reshape((15 * 15,))


def expand_pocliy_random(board: Board):
    board_array = board.get_board_array()
    conv_available = _convolve_board_available_narrow(board_array)
    cnt = conv_available.sum()
    probability = conv_available / cnt


    return_list = []
    for move in board.available:
        if conv_available[move]:
            return_list.append((move, probability[move]))

    return return_list


def rollout_policy_random(board: Board):
    board_array = board.get_board_array()
    conv_available = _convolve_board_available_narrow(board_array)
    probability = np.random.rand(15 * 15) * conv_available

    return probability


def expand_policy_network(board: Board) -> List[Tuple[int, float]]:
    board_array = board.get_board_array()
    probability = TreePolicyRunner(board_array)

    if len(board.moved) == 1:
        if board.moved[0] == move_xy2int(7, 7):
            return list(map(lambda move: (move, probability[move]), __second_move_available))
    if len(board.must[board.current_player]):
        return list(map(lambda move: (move, probability[move]), (board.must[board.current_player])))
    if len(board.must[0] | board.must[1]):
        return list(map(lambda move: (move, probability[move]), (board.must[0] | board.must[1])))

    conv_available = _convolve_board_available_wide(board_array)
    return_list = []

    for move in board.available:
        if conv_available[move]:
            return_list.append((move, probability[move]))

    return return_list


def rollout_policy_network(board: Board):
    probability = RolloutPolicyRunner(board.get_board_array())

    return probability


