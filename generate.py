
from scipy.fft import idct
import class_item 
import polygon
import math
import random
import unconvexpoligon as uc
import numpy as np
import time 
import sys

points = np.array([[6.09471997, 4.11162817],
 [4.0 ,         5.04845032], [4.6250296,  1.        ]])

sys.path.append('./smth2matrix')
sys.path.append('./shift_code')
from  shift2zero import shift2zero 

import pdb


class Generator():

    def __init__(self,  width, len, number):
        self.len = len
        self.width = width
        self.number = number

        self.data = []

        return

    def startRectangles(self, e):

   
        for id in range(self.number):
            x = random.gauss(3, 1.5) 
            y = random.gauss(3, 1.5)  
            points = np.array([[0, 0], [x, 0], [x, y], [0, y]])
            item = class_item.Item(id, points)
            item.set_matrix(e)
            long = max( len(item.matrix), len(item.matrix[0]) )

            while long*e > self.len or long*e > self.width :
                x = random.gauss(3, 1.5) 
                y = random.gauss(3, 1.5)   
                points = np.array([[0, 0], [x, 0], [x, y], [0, y]])
                item = class_item.Item(id, points)
                item.set_matrix(e)
                long = max( len(item.matrix), len(item.matrix[0]) )
            
            
            item.list_of_MixedShiftC_4R(e)
            self.data.append(item)
            

        return 

    def start(self, e):
        data = [] 
        # создаем
        for id in range(self.number):
            # t = time.time()
            
            points = np.array(uc.arpol(uc.getPolygon(), 0.0, 1, 4))
            size = shift2zero(points)

            x = random.uniform(e, self.width)
            y = random.uniform(e, self.len)
            x/=2
            y/=2
            for point in points:

                point[0]*=(x /size[0])
                point[1]*=(y /size[1])

            item = class_item.Item(id, points)
            item.list_of_MixedShiftC_4R(e)
            data.append(item)
            # print(item.matrix)
            # item.show_item(e)
            # for r in range(4):
                # print(item.listMatrix[r])
            # print( time.time() - t)
            # print(shift2zero(points))
        return data
        



if __name__ == "__main__":
    t = time.time()
    g = Generator(15, 15, 1)

    g.start(1)
    print(time.time() - t,'v')


