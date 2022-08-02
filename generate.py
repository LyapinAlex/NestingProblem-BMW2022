from scipy.fft import idct
import class_item 
import polygon
import math


class Generator():

    def __init__(self,  width, len, number):
        self.len = len
        self.width = width
        self.number = number

        self.data = []

        return

    def start(self, e):

        
        for id in range(self.number):
            points = polygon.getConvexPolygon(4, self.width, self.len).points
            item = class_item.Item(id, points)
            item.set_matrix_rectangular(e)
            # исправь для всех сторон
            long = max( len(item.matrix), len(item.matrix[0]) )
            while long > self.len or long > self.width:
                points = polygon.getConvexPolygon(3, self.width, self.len).points
                item = class_item.Item(id, points)
                item.set_matrix_rectangular(e)
                long = max( len(item.matrix), len(item.matrix[0]) )

            item.points = item.points.tolist()
            self.data.append(item)
            print("!!!!!!!!!", id)
            # print(item.matrix)

        
        return 


g = Generator(10, 10, 2)
g.start(0.5)