import class_item
import polygon
import math


class Generator():

    def __init__(self, len, width, number):
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
            maxLen = max(item.matrix.shape[0],item.matrix.shape[1])
            while maxLen  > self.width or maxLen > self.len:
                points = polygon.getConvexPolygon(4, self.width, self.len).points
                item = class_item.Item(id, points)
                item.set_matrix_rectangular(e)
                maxLen = max(item.matrix.shape[0],item.matrix.shape[1])
            self.data.append(item.matrix.tolist())

        
        return

