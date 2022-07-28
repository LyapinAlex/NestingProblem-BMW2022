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
                self.data.append(item)

        
        return

g = generate(10, 10, 1)
g.start()
for item in g.data:
    item.set_matrix( 0.5)
    print(item.matrix.shape)