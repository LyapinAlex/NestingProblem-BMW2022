from scipy.fft import idct
import class_item 
import polygon
import math
import random


class Generator():

    def __init__(self,  width, len, number):
        self.len = len
        self.width = width
        self.number = number

        self.data = []

        return

    def start(self, e):

        pp = random.randint(3, 6 )
        

        
        for id in range(self.number):
            points = polygon.getConvexPolygon(pp, self.width, self.len).points
            item = class_item.Item(id, points)
            item.set_matrix(e)
            # исправь для всех сторон
            long = max( len(item.matrix), len(item.matrix[0]) )
            S = sum(sum(item.matrix))*e*e

            while long*e > self.len or long*e > self.width or S < self.len* self.width / 10:
                points = polygon.getConvexPolygon(pp, self.width, self.len).points
                item = class_item.Item(id, points)
                item.set_matrix(e)
                long = max( len(item.matrix), len(item.matrix[0]) )
                S = sum(sum(item.matrix))*e*e
            item.points = item.points.tolist()
            self.data.append(item)

    

            minX = min([item.points[i][0] for i in range(3)])
            minY = min([item.points[i][1] for i in range(3)])
            for i in range(len(points)):
                item.points[i][0] = item.points[i][0] - minX
                item.points[i][1] = item.points[i][1] - minY


        
        return 


g = Generator(10, 10, 1)
g.start(0.5)

