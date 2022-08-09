import numpy as np


def simple2shift(matrix):
    ans = np.zeros(matrix.shape, dtype="int")
    for j in range(0, matrix.shape[1]):
        f = 0
        for i in range(matrix.shape[0] - 1, -1, -1):
            if matrix[i][j]: f += 1
            else: f = 0
            ans[i][j] = f
    return ans
