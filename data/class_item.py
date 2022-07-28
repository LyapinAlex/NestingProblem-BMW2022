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

    def set_matrix(self, h):
        x_max = 0.0
        y_max = 0.0
        for i in range(0, (self.points).shape[0]):
            x_max = max(x_max, self.points[i][0])
            y_max = max(y_max, self.points[i][1])
        x_min = x_max
        y_min = y_max
        for i in range(0, (self.points).shape[0]):
            x_min = min(x_min, self.points[i][0])
            y_min = min(y_min, self.points[i][1])

        self.matrix = np.ones((math.ceil(
            (x_max - x_min) / h), math.ceil((y_max - y_min) / h)),
                              dtype="int")
        
        # print("1235645")
        return None

    def set_rotation(self, rotate):
        self.rotation += rotate
        return None


# eq = Item(1, np.array([[0, 1], [0, 3], [3, 3.7], [2, 1.2]]))
# print(eq.points, ' ',eq.points.shape[0])
# eq.set_matrix(0.5)
# print(eq.matrix)
