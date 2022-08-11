import numpy as np
import math

if __name__=='__main__':
    from shift2zero import shift2zero
else:
    from .shift2zero import shift2zero



def polygon2matrix(points, h):
    # вычисление размера массива
    size_of_sides = shift2zero(points)
    n_x = math.ceil(size_of_sides[0] / h)
    n_y = math.ceil(size_of_sides[1] / h)

    # заполнение массива пересечений с осями параллельными оси абсцисс
    edges = np.zeros((n_x + 1, n_y))
    for k in range(0, n_y):
        for i in range(0, points.shape[0]):
            j = (i + 1) % points.shape[0]
            if ((min(points[i][1], points[j][1]) <= k * h)
                    and (k * h <= max(points[i][1], points[j][1]))):
                i1 = np.copy(points[i])  # i - номер точки i1
                i2 = np.copy(points[j])  # j - номер точки i2
                if (i2[1] - i1[1] == 0):  #ребро параллельно оси абсцисс
                    if (i1[0] > i2[0]):
                        fr = i1[0]
                        i1[0] = i2[0]
                        i2[0] = fr
                    edges[math.floor(i1[0] / h)][k] += 1.33
                    if (i2[0] % h != 0):
                        edges[math.floor(i2[0] / h + h / 100)][k] += 1.33
                    else:
                        edges[math.floor(i2[0] / h + h / 100)][k] += 1.33

                else:  #x+ay+b=0
                    a = -(i2[0] - i1[0]) / (i2[1] - i1[1])
                    b = -i1[0] - i1[1] * a
                    y_p = k * h
                    x_p = round(-b - a * k * h, 8)
                    # проверка положения по разные стороны
                    if (x_p == i1[0]):
                        # относительно первой точки
                        if ((i2[1] - y_p) *
                            (points[(i - 1) %
                                    (points).shape[0]][1] - y_p) < 0):
                            edges[math.floor(i1[0] / h + h / 100)][k] += 1
                        elif ((i2[1] - y_p) *
                              (points[(i - 1) %
                                      (points).shape[0]][1] - y_p) > 0):
                            edges[math.floor(i1[0] / h + h / 100)][k] += 2
                    elif (x_p != i2[0]):
                        edges[math.floor(x_p / h + h / 100)][k] += 1
    # создание растровой копии
    mat = np.zeros((n_x + 1, n_y + 1), dtype="int")
    for k in range(0, n_y):
        flag = 0.0
        for i in range(0, n_x + 1):
            if ((edges[i][k] % 2 == 0)
                    and (edges[i][k] != 0)):  #если наталкнулись на угол и т.п.
                mat[i][k] = 1
            elif (edges[i][k] % 2 == 1):  #если наталкнулись на пересечение
                mat[i][k] = 1
                if (k - 1 >= 0): mat[i][k - 1] = 1
                if (flag == 0): flag = 1
                else: flag = 0
            elif (edges[i][k] % 1 != 0):  #если наталкнулись на плотное косание
                if (k - 1 >= 0):
                    if (mat[i][k - 1] == 0):
                        mat[i][k] = 1
                    if ((flag == 0.5) and (i - 1 >= 0)):
                        if (mat[i - 1][k] == 1):
                            mat[i][k] = 1
                else:
                    mat[i][k] = 1
                if (flag == 0.5): flag = 0
                else: flag = 0.5
            if (flag > 0):  #заливка
                mat[i][k] = 1
                if ((flag == 1) and (k - 1 >= 0)):
                    mat[i][k - 1] = 1
    # закрашивание границ
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

if __name__=='__main__':
    print(polygon2matrix(np.array([[0,2.05],[0.26,0],[2.7,1.74]]), 1))