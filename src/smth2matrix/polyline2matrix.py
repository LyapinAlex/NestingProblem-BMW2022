import numpy as np
import math

if __name__=='__main__':
    from shift2zero import shift2zero
else:
    from .shift2zero import shift2zero



def polyline2matrix(points, h):
    # вычисление размера массива
    size_of_sides = shift2zero(points)
    n_x = math.ceil(size_of_sides[0] / h)
    n_y = math.ceil(size_of_sides[1] / h)

    mat = np.zeros((n_x + 1, n_y + 1), dtype="int")
    for i in range(0, (points).shape[0]):
        j = (i + 1) % (points).shape[0]
        i1 = np.copy(points[i])  # i - номер точки i1
        i2 = np.copy(points[j])  # j - номер точки i2

        j1 = [int(i1[0] / h), int(i1[1] / h)]  # пиксель соотв. i1 точке
        j2 = [int(i2[0] / h), int(i2[1] / h)]  # пиксель соотв. i2 точке

        step_x = 1
        step_y = 1
        check = 1
        if (j1[0] > j2[0]):
            step_x = -1
        elif (j1[0] == j2[0]):
            step_x = 0
        if (j1[1] > j2[1]):
            step_y = -1
            check = 0
        elif (j1[1] == j2[1]):
            step_y = 0

        p = [int(i1[0] / h), int(i1[1] / h)]  # двигается от j1 к j2
        if (j1[1] == j2[1]):  # вертикальная граница
            for i in range(0, abs(j1[0] - j2[0]) + 1):
                mat[p[0], p[1]] = 1
                p[0] += step_x
        else:
            for i in range(0, abs(j1[0] - j2[0]) + abs(j1[1] - j2[1]) + 1):
                mat[p[0], p[1]] = 1
                if (j2 != p):
                    a = -(i2[0] - i1[0]) / (i2[1] - i1[1])
                    b = -i1[0] - i1[1] * a
                    x_p = round(-b - a * (p[1] + check) * h, 8)
                    if (int(x_p / h) == p[0]):
                        p[1] += step_y
                    else:
                        p[0] += step_x
    mat = mat[0:n_x, 0:n_y]
    return mat
