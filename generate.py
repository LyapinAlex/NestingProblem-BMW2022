
from scipy.fft import idct
import class_item 
import polygon
import math
import random
import unconvexpoligon as uc
import numpy as np

class Generator():

    def __init__(self,  width, len, number):
        self.len = len
        self.width = width
        self.number = number

        self.data = []

        return


    def start(self, e):

        # pp = random.randint(3, 8)
        pp = 4

        # showPolygon(arpol(getPolygon(), 1.0, 2.0, 10))
   
        for id in range(self.number):
            points = np.array(uc.arpol(uc.getPolygon(), 3, 5, 4))
            item = class_item.Item(id, points)
            x = random.gauss(5, 1.5) 
            # print(item.points) 

            for point in item.points:
      
                point[0]*=x
                point[1]*=x
                
            item.set_matrix(e)
            # print(item.points) 
            # исправь для всех сторон
            long = max( len(item.matrix), len(item.matrix[0]) )
            
            S = sum(sum(item.matrix))*e*e

            while long*e > self.len or long*e > self.width :
            # while long*e > self.len or long*e > self.width or S < 1.0 :
                # print("!")
                points = uc.arpol(uc.getPolygon(),3 ,5, 4)
                item = class_item.Item(id, points)
                x = random.gauss(5, 1.5)    
                for point in item.points:
                    point[0]*=x
                    point[1]*=x
                item.set_matrix(e)
                long = max( len(item.matrix), len(item.matrix[0]) )
                S = sum(sum(item.matrix))*e*e

            # print(item.points)
            
            item.surfPoint()

            self.data.append(item)
           

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
            
            item.surfPoint()
    
            self.data.append(item)
           

        return 


g = Generator(10, 10, 1)
g.start(0.5)

