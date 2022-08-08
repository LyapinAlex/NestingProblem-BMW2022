import numpy as np


def simple2mixed_shift(matrix):
    ans = np.zeros(matrix.shape, dtype="int")
    for j in range(0, matrix.shape[1]):
        p = 0
        m = 0
        for i in range(matrix.shape[0] - 1, -1, -1):
            if matrix[i][j]:
                p += 1
                m = 0
                ans[i][j] = p
            else:
                p = 0
                m -= 1
                ans[i][j] = m
    return ans
