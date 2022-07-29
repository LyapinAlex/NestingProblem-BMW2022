import class_item
import polygon


class Generator():

    def __init__(self, len, width, number):
        self.len = len
        self.width = width
        self.number = number

        self.data = []

        return

    def start(self, e):

        if 1 :
            for id in range(self.number):
                points = polygon.getConvexPolygon(4, self.width, self.len).points
                item = class_item.Item(id, points)
                item.set_matrix_rectangular(e)
                # исправь для всех сторон
                while item.matrix.shape[0] > self.width or item.matrix.shape[1] > self.len:
                    points = polygon.getConvexPolygon(4, self.width, self.len).points
                    item = class_item.Item(id, points)
                    item.set_matrix_rectangular(e)
                self.data.append(item.matrix)

        
        return

