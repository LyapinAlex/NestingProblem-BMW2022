import class_item 
import polygon

class generate():

    def __init__(self, len, width, number):
        self.len = len
        self.width = width
        self.number = number
        self.data = []

        return

    def start(self):

        if 1 :
            for id in range(self.number):
                points = polygon.getConvexPolygon(5, self.width, self.len).points
                item = class_item.Item(id, points)
                item.list_of_MixedShiftC_4R(0.1)
        return
        

g = generate(10, 10, 1)
g.start()


