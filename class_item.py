import numpy as np
import matplotlib.pyplot as plt
import math
import copy
import time
from smth2matrix.polygon2matrix import polygon2matrix
from smth2matrix.polyline2matrix import polyline2matrix
from smth2matrix.shift2zero import shift2zero
from shift_code.simple2shift import simple2shift
from shift_code.simple2revers_shift import simple2revers_shift
from shift_code.simple2mixed_shift import simple2mixed_shift


class Item:

    def __init__(self,
                 id: int,
                 points: list,
                 lb_x: float = None,
                 lb_y: float = None,
                 pallet_number: int = None,
                 matrix: list = np.empty([0,0])):
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
                              dtype="int")
        return None

    def set_matrix(self, h):
        self.matrix = polygon2matrix(self.points, h)
        return None

    def matrix_of_border(self, h):
        mat = polyline2matrix(self.points, h)
        return mat

    def rotationMatrix(self):
        # self.rotation = math.ceil(rotate / math.pi * 90)
        # if (self.rotation % 90 == 0):
        #     self.matrix = np.rot90(self.matrix, self.rotation // 90)
        # else:
        #     print("Не прямой поворот:", self.rotation)
        self.matrix = np.rot90(self.matrix)

        return None

    def list_of_ShiftC_4R(self, h):  # крутит против часовой стрелки
        self.set_matrix(h)
        li = np.array(
            [[simple2revers_shift(self.matrix),
              simple2shift(self.matrix)], [None, None], [None, None],
             [None, None]])
        for i in range(1, 4):
            li[i][0] = simple2revers_shift(np.rot90(self.matrix, i))
            li[i][1] = simple2shift(np.rot90(self.matrix, i))
        return li

    def list_of_MixedShiftC_4R(self, h):  # крутит против часовой стрелки

        if self.empty_matrix():
            self.set_matrix(h)
        li = np.array([None, None, None, None])

        self.matix = self.matrix.transpose()

        for i in range(0, 4):
            li[i] = np.rot90(simple2mixed_shift(np.rot90(self.matrix, i - 1)))
            # li[i] = simple2mixed_shift(np.rot90(self.matrix, i ))
        self.matix = self.matrix.transpose()
        self.listMatrix = li
        return None

    
    def empty_matrix(self):
        return self.matrix.size == 0


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

    def surfPoint(self):
        # вычисление размера массива

        # self.points = self.points.tolist()

        minX = sorted(self.points, key=lambda point: point[0])[0][0]
        minY = sorted(self.points, key=lambda point: point[1])[0][1]

        # print(minX)
        for point in self.points:
            point[0] = point[0] - minX
            point[1] = point[1] - minY

        # self.points = np.array(self.points)
        return None


if (__name__=='__main__'):
    # start_time=time.time()
    # eq1 = Item(1, np.array([[1, 0], [0.3, 3], [3, 3.7], [2.1, 0]]))
    # eq1.list_of_MixedShiftC_4R(0.025)
    # print(time.time() - start_time, " seconds")
    # print(eq1.matrix.shape)


    start_time = time.time()
    eq2 = Item(1, np.array([[0.3, 0], [0, 1], [0.7, 1.5], [1.2, 0.8], [3, 0.8], [3, 0.4], [1.2, 0.4], [0.6, 0.8]]))
    # print(eq2.list_of_ShiftC_4R(0.025))
    eq2.list_of_MixedShiftC_4R(0.022)
    print("---", time.time() - start_time, "seconds ---")
