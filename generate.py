import unconvexpoligon as uc
import numpy as np
import class_item
import random
import sys

points = np.array([[6.09471997, 4.11162817],
 [4.0 ,         5.04845032], [4.6250296,  1.        ]])

sys.path.append('./smth2matrix')
sys.path.append('./shift_code')

from  shift2zero import shift2zero 
import pdb


class Generator():
    def __init__(self, width, len, number):
        self.len = len
        self.width = width
        self.number = number
        return

    def start(self, e):
        data = []
        for id in range(self.number):
            points = np.array(uc.arpol(uc.getPolygon(), 0.0, 1, 3))
            # print(points)
            size = shift2zero(points)
            # print(points)
            x = random.uniform(e, self.width)
            y = random.uniform(e, self.len)
            x/=2
            y /= 2
            


            for point in points:
                point[0] *= (x / size[0])
                point[1] *= (y / size[1])

            # print(points)
            item = class_item.Item(id, points)
            # print(item.points)
            item.list_of_MixedShiftC_4R(e)
            data.append(item)
            # print(item.matrix)
            # item.show_item(e)
            # for r in range(4):
            #     print(item.listMatrix[r])
            # print( time.time() - t)
            # print(shift2zero(points))
        return data
        


if __name__ == "__main__":
    import time
    t = time.time()
    g = Generator(10, 10, 1)

    g.start(1)
    print(time.time() - t, 'v')
