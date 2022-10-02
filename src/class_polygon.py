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
        self.area = self.calc_area()

    def __str__(self):
        s = ""
        for point in self.points:
            s += str(point) + " "
        return s

# -------------------------------  Structure   ---------------------------------

    def point(self, i):
        return self.points[i]

    def next(self, i):
        if i == self.num_sides - 1:
            return self.points[0]
        else:
            return self.points[i + 1]

    def prev(self, i):
        if i == 0:
            return self.points[self.num_sides - 1]
        else:
            return self.points[i - 1]

    def minXY(self):
        min_x = min(self.point(0).x, self.point(1).x)
        min_y = min(self.point(0).y, self.point(1).y)
        for i in range(2, self.num_sides):
            min_x = min(min_x, self.point(i).x)
            min_y = min(min_y, self.point(i).y)
        return Vector(min_x, min_y)

    def maxXY(self):
        max_x = max(self.point(0).x, self.point(1).x)
        max_y = max(self.point(0).y, self.point(1).y)
        for i in range(2, self.num_sides):
            max_x = max(max_x, self.point(i).x)
            max_y = max(max_y, self.point(i).y)
        return Vector(max_x, max_y)

    def sort_points(self):
        """Первой вершиной становится самая нижняя (если таких несколько, то из них самая левая), 
        дальше идут вершины против часовой стрелки"""
        num_first = 0
        first = self.point(0)
        for i in range(1, self.num_sides):
            if self.point(i) < first:
                num_first = i
                first = self.point(i)

        new_points = []
        is_clockwise = self.side_angle(num_first) > (
            p1.prev(num_first) - p1.point(num_first)).angle()
        if is_clockwise:
            for i in range(self.num_sides, 0, -1):
                new_points.append(self.point((i + num_first) % self.num_sides))
        else:
            for i in range(self.num_sides):
                new_points.append(self.point((i + num_first) % self.num_sides))
        self.points = new_points
        return self

    def resize(self):
        self.size = self.maxXY() - self.minXY()
        return self.size

    def round_points(self, ndigits=8):
        for point in self.points:
            point.x = round(point.x, ndigits)
            point.y = round(point.y, ndigits)
        return self

# ------------------------------  Calculations   -------------------------------

    def side_length(self, num_side):
        return abs(self.next(num_side) - self.point(num_side))

    def side_angle(self, num_side):
        return (self.next(num_side) - self.point(num_side)).angle()

    def calc_area(self, with_sign = False):
        area_value = 0
        for i in range(self.num_sides):
            area_value += self.point(i).x * self.next(i).y - self.next(i).x * self.point(i).y
        area_value /= 2
        if not with_sign: 
            area_value = abs(area_value)
        return area_value

    def area_circumscribed_rectangle(self):
        self.resize()
        return self.size.x * self.size.y

    def calc_centroid(self):
        centroid = Vector(0,0)
        for i in range(self.num_sides):
            area_value = self.point(i).x * self.next(i).y - self.next(i).x * self.point(i).y
            centroid.x = (self.point(i).x + self.next(i).x) * area_value
            centroid.y = (self.point(i).y + self.next(i).y) * area_value
        centroid /= 6 * self.calc_area(True)
        return centroid

    def choose_best_turn1(self):
        """Идея в минимизации разницы площадей фигуры и её растрового приближения"""
        target_value = 0
        target_side = 0
        for j in range(self.num_sides):
            new_value = 0
            for i in range(self.num_sides):
                new_value += self.side_length(i) * abs(
                    math.cos(2 * (self.side_angle(i) - self.side_angle(j))))
            if new_value > target_value:
                target_value = new_value
                target_side = j
        self.rotate_on_side(target_side)
        return self

    def choose_best_turn2(self):
        """Идея в минимизации площади описанного прямоугольника"""
        target_value = self.area_circumscribed_rectangle()
        target_side = 0
        for j in range(self.num_sides):
            self.rotate_on_side(j)
            new_value = self.area_circumscribed_rectangle()
            if new_value < target_value:
                target_value = new_value
                target_side = j
        self.rotate_on_side(target_side)
        return self

    def is_horizontal_intersection(self, num_side, height):
        """Пересекает ли сторона num_side прямую: y = height"""
        return (self.point(num_side).x - height) * (self.next(num_side).x -
                                                    height) < 0

    def is_horizontal(self, num_side):
        return self.point(num_side).y == self.next(num_side).y

    def is_vertical(self, num_side):
        return self.point(num_side).x == self.next(num_side).x

# -----------------------------  Rotate and move   -----------------------------

    def rotate(self, angle):
        for point in self.points:
            point.rotate(angle)
        self.round_points()
        return self

    def rotate_on_side(self, num_side):
        ang = self.side_angle(num_side)
        return self.rotate(-ang)

    def move_to(self, vector):
        shift_vector = vector - self.minXY()
        for point in self.points:
            point += shift_vector
        self.round_points()
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
            fig.set_figwidth(MAX_SIZE * self.size.x / self.size.y)
        else:
            fig.set_figheight(MAX_SIZE * self.size.y / self.size.x)
            fig.set_figwidth(MAX_SIZE)

        ax.set_xlim(self.minXY().x - 1, self.maxXY().x + 1)
        ax.set_ylim(self.minXY().y - 1, self.maxXY().y + 1)

        circumscribed_rectangle = patches.Rectangle(self.minXY().to_tuple(),
                                                    self.size.x,
                                                    self.size.y,
                                                    linewidth=2,
                                                    facecolor='none',
                                                    edgecolor='black')
        ax.add_patch(circumscribed_rectangle)

        polygon = patches.Polygon(self.points_to_list(),
                                  linewidth=1,
                                  edgecolor='red',
                                  fill=False)
        ax.add_patch(polygon)
        bar = self.calc_centroid()
        plt.plot(bar.x, bar.y,'co')
        plt.show()

if __name__ == '__main__':
    p1 = Polygon([
        Vector(3, 4),
        Vector(2, 2),
        Vector(0, 1),
        Vector(-4, 2),
        Vector(5, 13)
    ])
    # p1 = Polygon([
    #     Vector(1, 1),
    #     Vector(2, 2),
    #     Vector(3, 1),
    #     Vector(2, 0),
    # ])
    p1.sort_points().draw()
    p1.choose_best_turn1().draw()
    p1.choose_best_turn2().draw()
