import unconvexpoligon as uc
import numpy as np
import class_item
import random

from smth2matrix.shift2zero import shift2zero
from generators.generate_polygon1 import generate_polygon

class Generator():
    def __init__(self, width, len, number):
        self.len = len
        self.width = width
        self.number = number
        self.data = []
        return

    def start(self, e):
        for id in range(self.number):
            # t = time.time()
            points = generate_polygon(center=(250, 250), avg_radius=100, irregularity=0.35, spikiness=0.2, num_vertices=random.randint(3, 8))
            # points = np.array(uc.arpol(uc.getPolygon(), 0.0, 1, 3))
            size = shift2zero(points)

            x = random.uniform(e, self.width)
            y = random.uniform(e, self.len)
            x /= 2
            y /= 2
            for point in points:
                point[0] *= (x / size[0])
                point[1] *= (y / size[1])

            item = class_item.Item(id, points)
            item.list_of_MixedShiftC_4R(e)
            self.data.append(item)
        return


if __name__ == "__main__":
    import time
    t = time.time()
    g = Generator(10, 10, 1)
    g.start(1)
    print(time.time() - t, 'v')
