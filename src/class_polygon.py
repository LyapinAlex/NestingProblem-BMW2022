import math
from class_vector import Vector

import numpy as np
from matplotlib import patches
from matplotlib import pyplot as plt

class Polygon:
    def __init__(self, points):
        self.points = points
        self.num_sides = len(points)
        self.size = self.resize()
    
    def __str__(self):
        s = ""
        for point in self.points:
            s += str(point) + " "
        return s

# -------------------------------  Get point   ---------------------------------

    def point(self, i):
        return self.points[i]

    def next(self, i):
        if i == self.num_sides-1:
            return self.points[0]
        else:
            return self.points[i+1]
    
    def prev(self, i):
        if i == 0:
            return self.points[self.num_sides-1] 
        else:
            return self.points[i-1]

# ------------------------------  Calculations   -------------------------------

    def min(self):
        min_x = min(self.point(0).x, self.point(1).x)
        min_y = min(self.point(0).y, self.point(1).y)
        for i in range(2, self.num_sides):
            min_x = min(min_x, self.point(i).x)
            min_y = min(min_y, self.point(i).y)
        return Vector(min_x, min_y)

    def max(self):
        max_x = max(self.point(0).x, self.point(1).x)
        max_y = max(self.point(0).y, self.point(1).y)
        for i in range(2, self.num_sides):
            max_x = max(max_x, self.point(i).x)
            max_y = max(max_y, self.point(i).y)
        return Vector(max_x, max_y)

    def resize(self):
        self.size = self.max() - self.min()
        return self.size

    def side_length(self, num_side):
        return abs(p1.next(num_side)-p1.point(num_side))

    def side_angle(self, num_side):
        return (p1.next(num_side)-p1.point(num_side)).angle()

    def area_circumscribed_rectangle(self):
        self.resize()
        return self.size.x * self.size.y

# -----------------------------  Rotate and move   -----------------------------

    def rotate(self, angle):
        for point in self.points:
            point.rotate(angle)
        return self
    
    def rotate_on_side(self, num_side):
        ang = self.side_angle(num_side) + math.pi
        return self.rotate(-ang)

    def move_to(self, vector):
        shift_vector = vector - self.min()
        for point in self.points:
            point += shift_vector
        return self

    def move_to_origin(self):
        return self.move_to(Vector(0, 0))

# ---------------------------------  Output   ----------------------------------

    def points_to_list(self):
        list_of_points = []
        for point in self.points:
            list_of_points.append([point.x, point.y])
        return list_of_points

    def draw(self):
        fig, ax = plt.subplots()
        MAX_SIZE = 4
        self.resize()
        if self.size.x > self.size.y:
            fig.set_figheight(MAX_SIZE)
            fig.set_figwidth(MAX_SIZE * self.size.x/self.size.y)
        else:
            fig.set_figheight(MAX_SIZE * self.size.y/self.size.x)
            fig.set_figwidth(MAX_SIZE)

        ax.set_xlim( self.min().x - 1, self.max().x + 1 )
        ax.set_ylim( self.min().y - 1, self.max().y + 1 )

        circumscribed_rectangle = patches.Rectangle(self.min().to_tuple(), self.size.x, self.size.y, linewidth=2, facecolor='none', edgecolor='black')
        ax.add_patch(circumscribed_rectangle)

        polygon = patches.Polygon(self.points_to_list(), linewidth=1, edgecolor='red', fill=False)
        ax.add_patch(polygon)
        plt.show()


if __name__=='__main__':
    p1 = Polygon([Vector(3, 4), Vector(2, 2), Vector(0, 1), Vector(-4, 2), Vector(5, 13)])
    print(p1.area_circumscribed_rectangle())
    p1.draw()
    n = 2
    print(p1.side_length(n), p1.side_angle(n))
    p1.rotate_on_side(n)
    p1.move_to_origin()
    print(p1.side_length(n), p1.side_angle(n))
    print(p1.area_circumscribed_rectangle())
    p1.draw()
