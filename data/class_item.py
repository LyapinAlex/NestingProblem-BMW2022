import numpy as np
import math


class Item:

    def __init__(self, id, points):
        self.id = id
        self.points = points
        self.position = np.empty([0, 0])
        self.rotation = 0.0
        self.matrix = np.empty([0, 0])
        return None

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
                              dtype="int")

        return None

    def set_matrix(self, h):
        # вычисление размера массива
        x_max = max(self.points[0][0], self.points[1][0])
        x_min = min(self.points[0][0], self.points[1][0])
        y_max = max(self.points[0][1], self.points[1][1])
        y_min = min(self.points[0][1], self.points[1][1])
        for i in range(0, (self.points).shape[0]):
            x_max = max(x_max, self.points[i][0])
            y_max = max(y_max, self.points[i][1])
            x_min = min(x_min, self.points[i][0])
            y_min = min(y_min, self.points[i][1])

        n_x = math.ceil((x_max - x_min) / h)
        n_y = math.ceil((y_max - y_min) / h)
        # нормировка фигуры к (0,0)
        for i in range(0, (self.points).shape[0]):
            self.points[i][0] -= x_min
            self.points[i][1] -= y_min
        # заполнение массива пересечений с осями параллельными оси абсцисс
        for k in range(0,n_y):
            edges = np.zeros(n_x)
            intersect = []
            for i in range(0, (self.points).shape[0]):
                j = (i + 1) % (self.points).shape[0]
                if ((min(self.points[i][1], self.points[j][1]) <= k * h) and
                    (k * h <= max(self.points[i][1], self.points[j][1]))):
                    i1 = np.copy(self.points[i])
                    i2 = np.copy(self.points[j])
                    # print(i, i1, j, i2) # i - номер точки i1 
                    if (i2[1] - i1[1] == 0): #ребро параллельно оси абсцисс
                        if (i1[0] > i2[0]):
                            fr = i1[0]
                            i1[0] = i2[0]
                            i2[0] = fr
                        for m in range (math.floor(i1[0]/h),math.floor(i2[0]/h)):
                            edges[m] = +1.33
                        if (i2[0]%h!=0): edges[math.floor(i2[0]/h)] = +1.33

                    else:  #x+ay+b=0
                        a = -(i2[0] - i1[0]) / (i2[1] - i1[1])
                        b = (-i1[0] * (i2[1] - i1[1]) + i1[1] *
                             (i2[0] - i1[0])) / (i2[1] - i1[1])
                        y_p = k * h
                        x_p = -b - a * k * h
                        # проверка положения по разные стороны
                        if (x_p == i1[0]): 
                            # относительно первой точки
                            if ( (i2[1]-y_p) * (self.points[(i - 1) % (self.points).shape[0]][1]-y_p) < 0 ):
                                edges[math.floor(i1[0]/h)] += 1
                            else: edges[math.floor(i1[0]/h)] += 2
                        elif (x_p != i2[0]):
                            edges[math.floor(x_p/h)] += 1
                        intersect.append([x_p, i1, i2])
            print(edges)
                    
            #print()
            intersect = sorted(intersect, key=lambda inter: inter[0])
            #print(intersect)
        
        # создание массива
        self.matrix = np.zeros((n_x, n_y), dtype="int")

        return None

    def set_rotation(self, rotate):
        self.rotation = math.ceil(rotate / math.pi * 90)
        if (self.rotation % 90 == 0):
            self.matrix = np.rot90(self.matrix, self.rotation // 90)
        else:
            print("Не прямой поворот:", self.rotation)
        return None


eq = Item(1, np.array([[1, 0], [0, 3], [3, 3.7], [2.1, 0]]))
## print(eq.points, ' ', eq.points.shape[0])
eq.set_matrix(0.5)
# print(eq.matrix)
# print(eq.points)
