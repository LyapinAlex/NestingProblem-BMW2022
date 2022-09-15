import numpy as np


def classic2new_shift(matrix):
    line_code = np.full(matrix.shape[0], None, dtype=list)
    for j in range(0, matrix.shape[0]):
        pred = matrix[j][0]
        sum = 1
        line = []
        for i in range(1, matrix.shape[1]):
            if matrix[j][i] == pred:
                sum += 1
            else:
                if not pred: sum *= -1
                line.append(sum)
                pred = matrix[j][i]
                sum = 1
        if not pred: sum *= -1
        line.append(sum)
        line_code[j] = line
    return line_code