import numpy as np
import matplotlib.pyplot as plt
import math


class Item:

    def __init__(self, id: int, points: list, lb_x: float = None, lb_y: float = None,
                 pallet_number: int = None, matrix: list = None):
        self.id = id
        self.points = points
        self.lb_x = lb_x
        self.lb_y = lb_y
        self.pallet_number = pallet_number
        self.rotation = 0.0
        self.matrix = matrix

    def set_matrix_rectangular(self, h):
        x_max = max(self.points[0][0], self.points[1][0])
        x_min = min(self.points[0][0], self.points[1][0])
        y_max = max(self.points[0][1], self.points[1][1])
        y_min = min(self.points[0][1], self.points[1][1])
        for i in range(0, (self.points).shape[0]):
            x_max = max(x_max, self.points[i][0])
            y_max = max(y_max, self.points[i][1])
            x_min = min(x_min, self.points[i][0])
            y_min = min(y_min, self.points[i][1])

        self.matrix = np.ones((math.ceil(
            (x_max - x_min) / h), math.ceil((y_max - y_min) / h)),
                              dtype="int").tolist()
        
        return None

    def shift2zero(self):
        # сдвиг фигуры к началу координат
        x_max = max(self.points[0][0], self.points[1][0])
        x_min = min(self.points[0][0], self.points[1][0])
        y_max = max(self.points[0][1], self.points[1][1])
        y_min = min(self.points[0][1], self.points[1][1])
        for i in range(0, (self.points).shape[0]):
            x_max = max(x_max, self.points[i][0])
            y_max = max(y_max, self.points[i][1])
            x_min = min(x_min, self.points[i][0])
            y_min = min(y_min, self.points[i][1])
        # нормировка фигуры к (0,0)
        for i in range(0, (self.points).shape[0]):
            self.points[i][0] -= x_min
            self.points[i][1] -= y_min
        return [x_min, x_max, y_min, y_max]

    def set_matrix(self, h):
        # вычисление размера массива
        size_of_sides = self.shift2zero()
        n_x = math.ceil((size_of_sides[1] - size_of_sides[0]) / h)
        n_y = math.ceil((size_of_sides[3] - size_of_sides[2]) / h)

        # заполнение массива пересечений с осями параллельными оси абсцисс
        edges = np.zeros((n_x + 1, n_y))
        for k in range(0, n_y):
            for i in range(0, (self.points).shape[0]):
                j = (i + 1) % (self.points).shape[0]
                if ((min(self.points[i][1], self.points[j][1]) <= k * h) and
                    (k * h <= max(self.points[i][1], self.points[j][1]))):
                    i1 = np.copy(self.points[i])  # i - номер точки i1
                    i2 = np.copy(self.points[j])  # j - номер точки i2
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
                                (self.points[(i - 1) %
                                             (self.points).shape[0]][1] - y_p)
                                    < 0):
                                edges[math.floor(i1[0] / h + h / 100)][k] += 1
                            elif (
                                (i2[1] - y_p) *
                                (self.points[(i - 1) %
                                             (self.points).shape[0]][1] - y_p)
                                    > 0):
                                edges[math.floor(i1[0] / h + h / 100)][k] += 2
                        elif (x_p != i2[0]):
                            edges[math.floor(x_p / h + h / 100)][k] += 1
                            #print(i1, i2, x_p)
        # print(edges)
        # создание растровой копии
        self.matrix = np.zeros((n_x + 1, n_y + 1), dtype="int")
        for k in range(0, n_y):
            flag = 0.0
            for i in range(0, n_x + 1):
                if ((edges[i][k] % 2 == 0) and
                    (edges[i][k] != 0)):  #если наталкнулись на угол и т.п.
                    self.matrix[i][k] = 1
                elif (edges[i][k] % 2 == 1):  #если наталкнулись на пересечение
                    self.matrix[i][k] = 1
                    if (k - 1 >= 0): self.matrix[i][k - 1] = 1
                    if (flag == 0): flag = 1
                    else: flag = 0
                elif (edges[i][k] % 1 !=
                      0):  #если наталкнулись на плотное косание
                    if (k - 1 >= 0):
                        if (self.matrix[i][k - 1] == 0):
                            self.matrix[i][k] = 1
                        if ((flag == 0.5) and (i - 1 >= 0)):
                            if (self.matrix[i - 1][k] == 1):
                                self.matrix[i][k] = 1
                    else:
                        self.matrix[i][k] = 1
                    if (flag == 0.5): flag = 0
                    else: flag = 0.5
                if (flag > 0):  #заливка
                    self.matrix[i][k] = 1
                    if ((flag == 1) and (k - 1 >= 0)):
                        self.matrix[i][k - 1] = 1
        # закрашивание границ
        for i in range(0, (self.points).shape[0]):
            j = (i + 1) % (self.points).shape[0]
            i1 = np.copy(self.points[i])  # i - номер точки i1
            i2 = np.copy(self.points[j])  # j - номер точки i2

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
                    self.matrix[p[0], p[1]] = 1
                    p[0] += step_x
            else:
                for i in range(0, abs(j1[0] - j2[0]) + abs(j1[1] - j2[1]) + 1):
                    self.matrix[p[0], p[1]] = 1
                    if (j2 != p):
                        a = -(i2[0] - i1[0]) / (i2[1] - i1[1])
                        b = -i1[0] - i1[1] * a
                        x_p = round(-b - a * (p[1] + check) * h, 8)
                        if (int(x_p / h) == p[0]):
                            p[1] += step_y
                        else:
                            p[0] += step_x
        self.matrix = self.matrix[0:n_x, 0:n_y]
        return None

    # def set_rotation(self, rotate):
    #     self.rotation = math.ceil(rotate / math.pi * 90)
    #     if (self.rotation % 90 == 0):
    #         self.matrix = np.rot90(self.matrix, self.rotation // 90)
    #     else:
    #         print("Не прямой поворот:", self.rotation)
    #     return None

    def rotation90_item_matrix(self): 
  
        self.matrix = np.rot90(np.array(self.matrix))
        self.matrix = self.matrix.tolist()

    def matrix_of_border(self, h, n_x, n_y):
        mat = np.zeros((n_x + 1, n_y + 1), dtype="int")
        for i in range(0, (self.points).shape[0]):
            j = (i + 1) % (self.points).shape[0]
            i1 = np.copy(self.points[i])  # i - номер точки i1
            i2 = np.copy(self.points[j])  # j - номер точки i2

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

    def show_item(self):
        pointsX = []
        pointsY = []
        
        for point in self.points:
            pointsX.append(point[0])
            pointsY.append(point[1])
        

        pointsX.append(self.points[0][0])
        pointsY.append(self.points[0][1])
                
        plt.plot(np.array(pointsX), np.array(pointsY), '-k')
                

        plt.show()
        return

    


# eq = Item(1, np.array([[0, 1], [0, 3], [3, 3.7], [7, 1.2]]))
# print(eq.points, ' ', eq.points.shape[0])
# eq.set_matrix_rectangular(0.5)
# print(eq.matrix)
# eq.set_rotation(1.5707*2)
# print(eq.matrix)
