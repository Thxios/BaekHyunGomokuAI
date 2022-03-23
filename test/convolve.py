import scipy.signal
import numpy as np


board = np.zeros((15, 15))
board[7, 7] = 1
board[7, 8] = 1
board[8, 8] = 1
print(board)

kernel = np.array([
    [1, 0, 0, 1, 0, 0, 1],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [1, 0, 0, 1, 0, 0, 1],
])

can = scipy.signal.convolve2d(board, kernel, 'same')
print(can)


