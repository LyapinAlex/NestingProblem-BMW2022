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

    def set_rotation(self, rotate):
        self.rotation = math.ceil(rotate / math.pi * 90)
        if (self.rotation % 90 == 0):
            self.matrix = np.rot90(self.matrix, self.rotation // 90)
        else:
            print("Не прямой поворот")
        return None


# eq = Item(1, np.array([[0, 1], [0, 3], [3, 3.7], [7, 1.2]]))
# print(eq.points, ' ', eq.points.shape[0])
# eq.set_matrix_rectangular(0.5)
# print(eq.matrix)
# eq.set_rotation(1.5707*2)
# print(eq.matrix)
