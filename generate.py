
from scipy.fft import idct
import class_item 
import polygon
import math
import random
import unconvexpoligon as uc
import numpy as np
import time 
import sys

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
        
        # создаем
        for id in range(self.number):
            # t = time.time()
            
            points = np.array(uc.arpol(uc.getPolygon(), 0.0, 1, 3))
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
            self.data.append(item)
            # print( time.time() - t)
            # print(shift2zero(points))
        return
        



if __name__ == "__main__":
    t = time.time()
    g = Generator(20, 10, 1)

    g.start(0.1)
    print(time.time() - t,'v')


