import numpy as np
from math import ceil, floor

if __name__=='__main__':
    from shift2zero import shift2zero
else:
    from .shift2zero import shift2zero

def polygon2matrix(points, h):
    _INACCURACY = h * 0.000001 # нужна для исправления ошибки округления при вычислениях
    # вычисление размера массива
    size_of_sides = shift2zero(points)
    n_x = ceil(size_of_sides[0] / h)
    n_y = ceil(size_of_sides[1] / h)

    # заполнение массива пересечений с осями параллельными оси абсцисс
    edges = np.zeros((n_x + 1, n_y), dtype='int')
    for k in range(0, n_y):
        for i0 in range(0, points.shape[0]):
            i1 = (i0 + 1) % points.shape[0] # "% points.shape[0]" использую чтоб зациклить точки (случай первой и последней точки)
            if (min(points[i0][1], points[i1][1]) <= k * h) and (k * h <= max(points[i0][1], points[i1][1])) and (points[i1][1] != points[i0][1]):
                a = -(points[i1][0] - points[i0][0]) / (points[i1][1] - points[i0][1])
                b = -points[i0][0] - points[i0][1] * a
                y_p = k * h
                x_p = round(-b - a * k * h, 8)
                # проверка положения по разные стороны
                if (x_p == points[i0][0]):
                    # относительно первой точки
                    if ((points[i1][1] - y_p) * (points[(i0 - 1) % points.shape[0]][1] - y_p) < 0):
                        edges[floor(x_p / h + _INACCURACY)][k] += 1
                    elif ((points[i1][1] - y_p) * (points[(i0 - 1) % points.shape[0]][1] - y_p) > 0):
                        edges[floor(x_p / h + _INACCURACY)][k] += 2
                elif (x_p != points[i1][0]):
                    edges[floor(x_p / h + _INACCURACY)][k] += 1

    # закрашивание внутренности и почти всей границы
    mat = np.zeros((n_x + 1, n_y + 1), dtype="int")
    for k in range(n_y):
        flag = False
        for i in range(n_x + 1):
            if ((edges[i][k] % 2 == 0) and (edges[i][k] != 0)):  #если наталкнулись на угол и т.п.
                mat[i][k] = 1
            elif (edges[i][k] % 2 == 1):  #если наталкнулись на пересечение
                mat[i][k] = 1
                if k: mat[i][k - 1] = 1 # проверка на не выход за границы массива
                flag = not flag 
            if flag:  #заливка
                mat[i][k] = 1
                if k: mat[i][k - 1] = 1 # проверка на не выход за границы массива
    
    # закрашивание границ
    for i in range(0, (points).shape[0]):
        j = (i + 1) % (points).shape[0]
        i1 = np.copy(points[i])  # i - номер точки i1
        i2 = np.copy(points[j])  # j - номер точки i2

        j1 = [int(i1[0] / h), int(i1[1] / h)]  # пиксель соотв. i1 точке
        j2 = [int(i2[0] / h), int(i2[1] / h)]  # пиксель соотв. i2 точке

        step_x = 1
        step_y = 1
        check = 1 # смотрим на пересечение с верхней линеей (x_p)
        if (j1[0] > j2[0]):
            step_x = -1
        elif (j1[0] == j2[0]):
            step_x = 0
        if (j1[1] > j2[1]):
            step_y = -1
            check = 0 # смотрим на пересечение с нижней линеей (x_p)
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
    mat = mat[0:n_x, 0:n_y] #срез матрицы
    return mat

if __name__=='__main__':
    print(polygon2matrix(np.array([[1, 0], [0.3, 3], [3, 3.7], [2.1, 0]]), 2.6))