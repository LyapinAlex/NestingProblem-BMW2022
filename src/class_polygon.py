from copy import deepcopy
import math
import random
from queue import Queue
import numpy as np
from math import ceil, floor
from matplotlib import patches
from matplotlib import pyplot as plt
from class_DCEL import DCEL
from class_arrangement import draw_segments_sequence
from class_direction import is_convex, isBetween
from class_segment import Segment

from class_vector import Vector


class Polygon:

    def __init__(self, points):
        if type(points[0]) == type(Vector(0, 0)):
            self.points = points
        else:
            self.points = []
            for point in points:
                self.points.append(Vector(point[0], point[1]))
        self.num_sides = len(points)
        self.size = self.resize()
        self.area = self.calc_area()
        self.expanded_polygon = None
        self.max_XY = self.maxXY()
        self.min_XY = self.minXY()

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

    def get_side(self, num_side):
        """-1 <= num_side <= self.num_sides"""
        if num_side == self.num_sides:
            return self.next(0) - self.point(0)
        elif num_side == -1:
            return self.point(0) - self.prev(0)
        else:
            return self.next(num_side) - self.point(num_side)

    def next_index(self, i):
        return (i+1) % len(self.points)

    def prev_index(self, i):
        if i == 0:
            return len(self.points)-1
        return i-1

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

    def resize(self):
        self.size = self.maxXY() - self.minXY()
        self.max_XY = self.maxXY()
        self.min_XY = self.minXY()
        return self.size

    def round_points(self, ndigits=4):
        for point in self.points:
            point.x = round(point.x, ndigits)
            point.y = round(point.y, ndigits)
        return self

# ---------------------------  Structure changes  -----------------------------

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
            self.prev(num_first) - self.point(num_first)).angle()
        if is_clockwise:
            for i in range(self.num_sides, 0, -1):
                new_points.append(self.point((i + num_first) % self.num_sides))
        else:
            for i in range(self.num_sides):
                new_points.append(self.point((i + num_first) % self.num_sides))
        self.points = new_points
        return

    def del_points_on_one_line(self):
        if not Vector.is_collinear(self.get_side(0),
                                   self.get_side(self.num_sides - 1)):
            new_points = [self.points[0]]
        else:
            new_points = []
        for i in range(1, self.num_sides):
            if not Vector.is_collinear(self.get_side(i), self.get_side(i - 1)):
                new_points.append(self.point(i))
        self.points = new_points
        self.num_sides = len(self.points)
        return

    def del_duplicate_points(self):
        new_points = [self.points[0]]
        new_prev_point = self.points[0]
        for i in range(1, self.num_sides):
            if not abs(new_prev_point -
                       self.point(i)) < 0.001:  # длина меньше микромерта
                new_points.append(self.point(i))
                new_prev_point = self.points[i]
        self.points = new_points
        self.num_sides = len(self.points)
        return

    def bring_points2normal_appearance(self):
        """Удаляет дублирующиеся точки, потом удаляет среднюю из трёх соседствующих точек лежащих на одной прямой, 
        далее упорядочивает их так, что первой вершиной становится самая нижняя (если таких несколько, то из них самая левая), 
        дальше идут вершины против часовой стрелки"""
        # self.del_duplicate_points()
        # self.del_points_on_one_line()
        # self.sort_points()
        return

# ------------------------------  Calculations   -------------------------------

    def side_length(self, num_side):
        return abs(self.get_side(num_side))

    def side_angle(self, num_side):
        return self.get_side(num_side).angle()

    def calc_area(self, without_sign=True):
        area_value = 0
        for i in range(self.num_sides):
            area_value += self.point(i).x * self.next(i).y - self.next(
                i).x * self.point(i).y
        area_value /= 2
        if without_sign:
            area_value = abs(area_value)
        return area_value

    def area_circumscribed_rectangle(self):
        self.resize()
        return self.size.x * self.size.y

    def calc_centroid(self):
        centroid = Vector(0,  0)
        for i in range(self.num_sides):
            area_value = self.point(i).x * self.next(i).y - self.next(
                i).x * self.point(i).y
            centroid.x += (self.point(i).x + self.next(i).x) * area_value
            centroid.y += (self.point(i).y + self.next(i).y) * area_value
        centroid /= 6 * self.calc_area(False)
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

    def choose_best_turn3(self):
        """Кладём мредмет на длиннейшую сторону"""
        target_value = 0
        target_side = 0
        for j in range(self.num_sides):
            if self.side_length(j) > target_value:
                target_value = self.side_length(j)
                target_side = j
        self.rotate_on_side(target_side)
        return self

    def expand_polygon(self, indent):
        self.bring_points2normal_appearance()
        exp_points = []
        for i in range(self.num_sides):
            v1 = self.get_side(i - 1).normalize()
            v2 = -self.get_side(i).normalize()
            v = (v1 + v2)
            v *= indent / math.sin(math.pi - (v1.angle() - v2.angle()))
            exp_points.append(self.point(i) + v)
        return Polygon(exp_points)

    def is_side_horizontal(self, num_side):
        return self.point(num_side).y == self.next(num_side).y

    def is_side_vertical(self, num_side):
        return self.point(num_side).x == self.next(num_side).x

    def is_side_intersect_horizontal(self, num_side, height):
        """Пересекает ли сторона num_side прямую: y = height"""
        return (self.point(num_side).y - height) * (self.next(num_side).y -
                                                    height) <= 0

    def intersection_side_and_horizontal(self, num_side, height):
        """Точка пересечения стороны num_side и прямой: y = height"""
        if not self.is_side_horizontal(num_side):
            a = -(self.next(num_side).x - self.point(num_side).x) / (
                self.next(num_side).y - self.point(num_side).y)
            b = -self.point(num_side).x - self.point(num_side).y * a
            y_p = height
            x_p = round(-b - a * height, 8)
            return Vector(x_p, y_p)
        else:
            return None

# ---------------------------------  Rastr   ---------------------------------

    def create_rastr_array_edges(self, h: float):
        """Создаёт массив пересечений рёбер с горизонтальными прямыми для дальнейшего создания растрового приближения"""
        _INACCURACY = h * 0.000001  # нужна для исправления ошибки округления при вычислениях
        self_copy = self.copy().move_to_origin()
        n_x = ceil(self_copy.size.x / h)
        n_y = ceil(self_copy.size.y / h)
        edges = np.zeros((n_y, n_x + 1), dtype='int')

        # заполнение массива пересечений с осями параллельными оси абсцисс
        for k in range(0, n_y):
            for num_side in range(0, self_copy.num_sides):
                if self_copy.is_side_intersect_horizontal(
                        num_side,
                        k * h) and not self_copy.is_side_horizontal(num_side):
                    intersect_point = self_copy.intersection_side_and_horizontal(
                        num_side, k * h)
                    if (intersect_point.x == self_copy.point(num_side).x):
                        # проверка положения по разные стороны
                        if ((self_copy.next(num_side).y - intersect_point.y) *
                            (self_copy.prev(num_side).y - intersect_point.y) <
                                0):
                            edges[k][floor(intersect_point.x / h +
                                           _INACCURACY)] += 1
                        elif (
                            (self_copy.next(num_side).y - intersect_point.y) *
                            (self_copy.prev(num_side).y - intersect_point.y) >
                                0):
                            edges[k][floor(intersect_point.x / h +
                                           _INACCURACY)] += 2
                    elif (intersect_point.x != self_copy.next(num_side).x):
                        edges[k][floor(intersect_point.x / h +
                                       _INACCURACY)] += 1
        return edges

    def rastr_painting_over_inside(self, edges):
        """Создаёт растровое приближение для многоугольника"""
        rastr_approximation = np.zeros((edges.shape[0] + 1, edges.shape[1]),
                                       dtype="int")
        for k in range(edges.shape[0]):
            flag = False
            for i in range(edges.shape[1]):
                if ((edges[k][i] % 2 == 0) and
                        (edges[k][i] != 0)):  # если наталкнулись на угол и т.п.
                    rastr_approximation[k][i] = 1
                elif (edges[k][i] % 2 == 1):  # если наталкнулись на пересечение
                    rastr_approximation[k][i] = 1
                    if k:
                        rastr_approximation[k - 1][
                            i] = 1  # проверка на не выход за границы массива
                    flag = not flag
                if flag:  # заливка
                    rastr_approximation[k][i] = 1
                    if k:
                        rastr_approximation[k - 1][
                            i] = 1  # проверка на не выход за границы массива
        return rastr_approximation

    def create_rastr_border(self, h: float, rastr_approximation=None):
        """Создаёт растровый контур многоугольника"""
        self_copy = self.copy().move_to_origin()
        if type(rastr_approximation) == type(None):
            n_x = ceil(self_copy.size.x / h) + 1
            n_y = ceil(self_copy.size.y / h) + 1
            rastr_approximation = np.zeros((n_y, n_x), dtype="int")
        else:
            n_x = rastr_approximation.shape[1]
            n_y = rastr_approximation.shape[0]

        for num_side in range(0, self_copy.num_sides):
            p1 = self_copy.point(num_side)
            p2 = self_copy.next(num_side)

            rp1 = Vector(int(p1.x / h),
                         int(p1.y / h))  # пиксель соотв. p1 точке
            rp2 = Vector(int(p2.x / h),
                         int(p2.y / h))  # пиксель соотв. p2 точке

            direction_of_movement = Vector(1, 1)
            direction_of_movement.x = 1
            direction_of_movement.y = 1
            check = 1  # смотрим на пересечение с верхней линеей (x_p)
            if (rp1.x > rp2.x):
                direction_of_movement.x = -1
            elif (rp1.x == rp2.x):
                direction_of_movement.x = 0
            if (rp1.y > rp2.y):
                direction_of_movement.y = -1
                check = 0  # смотрим на пересечение с нижней линеей (x_p)
            elif (rp1.y == rp2.y):
                direction_of_movement.y = 0

            p = rp1.copy()  # двигается от rp1 к rp2
            if (rp1.y == rp2.y):  # вертикальная граница
                for i in range(0, abs(rp1.x - rp2.x) + 1):
                    rastr_approximation[p.y, p.x] = 1
                    p.x += direction_of_movement.x
            else:
                for i in range(0, abs(rp1.x - rp2.x) + abs(rp1.y - rp2.y) + 1):
                    rastr_approximation[p.y, p.x] = 1
                    if (rp2 != p):
                        a = -(p2.x - p1.x) / (p2.y - p1.y)
                        b = -p1.x - p1.y * a
                        x_p = round(-b - a * (p.y + check) * h, 8)
                        if (int(x_p / h) == p.x):
                            p.y += direction_of_movement.y
                        else:
                            p.x += direction_of_movement.x
        return rastr_approximation[0:n_y - 1, 0:n_x - 1]  # срез матрицы

    def create_rastr_approximation(self, h: float):
        edges = self.create_rastr_array_edges(h)
        rastr_approximation = self.rastr_painting_over_inside(edges)
        rastr_approximation = self.create_rastr_border(h, rastr_approximation)
        return rastr_approximation
# -----------------------------  NFP   -----------------------------------------

    @staticmethod
    def reduced_convolution(p1: 'Polygon', p2: 'Polygon'):
        reduced_convolution = []
        n1 = len(p1.points)
        n2 = len(p2.points)

        if (n1 == 0 or n2 == 0):
            return []
        visited_states = set()
        state = Queue()
        for i in range(n1-1, -1, -1):
            state.put((i, 0))
        while (not state.empty()):
            current_state = state.get()
            i1 = current_state[0]
            i2 = current_state[1]
            if (current_state in visited_states):
                continue
            visited_states.add(current_state)

            next_i1 = p1.next_index(i1)
            next_i2 = p2.next_index(i2)
            prev_i1 = p1.prev_index(i1)
            prev_i2 = p2.prev_index(i2)

            for step in (False, True):
                new_i1 = 0
                new_i2 = 0
                if (step):
                    new_i1 = next_i1
                    new_i2 = i2
                else:
                    new_i1 = i1
                    new_i2 = next_i2
                belong_to_convolution = False
                if (step):
                    belong_to_convolution = isBetween(
                        p1.point(next_i1)-p1.point(i1), p2.point(i2)-p2.point(prev_i2), p2.point(next_i2)-p2.point(i2))
                else:
                    belong_to_convolution = isBetween(p2.point(next_i2)-p2.point(i2), p1.point(i1) -
                                                      p1.point(prev_i1), p1.point(next_i1)-p1.point(i1))
                if (belong_to_convolution):
                    state.put((new_i1, new_i2))
                    convex = False
                    if (step):
                        convex = is_convex(p2.point(prev_i2),
                                           p2.point(i2), p2.point(next_i2))
                    else:
                        convex = is_convex(p1.point(prev_i1),
                                           p1.point(i1), p1.point(next_i1))
                    if (convex):
                        start_point = p1.point(i1)+p2.point(i2)
                        end_point = p1.point(new_i1)+p2.point(new_i2)
                        reduced_convolution.append(
                            Segment(start_point, end_point))
        return reduced_convolution

    @staticmethod
    def minkowski_sum_arrangement(p1: 'Polygon', p2: 'Polygon'):
        p2.sort_points()
        reduce_conv = Polygon.reduced_convolution(p1, p2)
        arrangement_without_translate = DCEL(reduce_conv)  # Костыль
        max_point_b = arrangement_without_translate.vertices.max_key_node(
            arrangement_without_translate.vertices.root).key
        max_point_a = Vector(-1000000, -1000000)

        for point in p1.points:
            if (point > max_point_a):
                max_point_a = point

        segments_with_translate = []
        for half_edge in arrangement_without_translate.half_edges:
            half_edge.is_visited = False

        for half_edge in arrangement_without_translate.half_edges:
            if (half_edge.is_visited):
                continue
            half_edge.is_visited = True
            half_edge.twin.is_visited = True
            segments_with_translate.append(
                Segment(half_edge.origin, half_edge.end))

        for segment in segments_with_translate:  # Когда писал += почему то происходил баг
            segment.min_point = segment.min_point + \
                (max_point_a-max_point_b)
            segment.max_point = segment.max_point + \
                (max_point_a-max_point_b)

        arrangement = DCEL(segments_with_translate)

        return arrangement

    @staticmethod
    def nfp(p1: 'Polygon', p2: 'Polygon'):
        minus_points = []

        for point in p2.points:
            minus_points.append(point*(-1))

        no_fit_polygon = Polygon.minkowski_sum_arrangement(
            p1, Polygon(minus_points))
        # Костыль
        boundary_half_edge = no_fit_polygon.unbounded_face.holes_half_edges[0]
        edges = []
        edges.append(
            Segment(boundary_half_edge.origin, boundary_half_edge.end))
        current_half_edge = boundary_half_edge.next
        while (current_half_edge != boundary_half_edge):
            edges.append(
                Segment(current_half_edge.origin, current_half_edge.end))
            current_half_edge = current_half_edge.next

        new_nfp = DCEL(edges)

        return new_nfp

    # -----------------------------  Rotate and move   -----------------------------

    def rotate(self, angle):
        for point in self.points:
            point.rotate(angle)
        self.resize()
        return self

    def rotate_on_side(self, num_side):
        ang = self.side_angle(num_side)
        return self.rotate(-ang)

    def move_to(self, vector):
        shift_vector = vector - self.minXY()
        for point in self.points:
            point += shift_vector
        return self

    def move_to_origin(self):
        return self.move_to(Vector(0, 0))

# ---------------------------------   Output   ---------------------------------

    def copy(self):
        new_points = []
        for point in self.points:
            new_points.append(point.copy())
        return Polygon(new_points)

    def points_to_list(self):
        list_of_points = []
        for point in self.points:
            list_of_points.append([point.x, point.y])
        return list_of_points

    def points_to_array(self):
        return np.array(self.points_to_list())

    def draw(self,
             indent_expand_polygon=0.5,
             is_draw_raster_approximation=False,
             h=None):

        # ----------   background   ----------

        fig, ax = plt.subplots()
        MAX_SIZE = 4
        self.resize()
        if self.size.x > self.size.y:
            fig.set_figheight(MAX_SIZE)
            fig.set_figwidth(MAX_SIZE * self.size.x / self.size.y)
        else:
            fig.set_figheight(MAX_SIZE * self.size.y / self.size.x)
            fig.set_figwidth(MAX_SIZE)

        fig.set_figheight(MAX_SIZE)
        fig.set_figwidth(MAX_SIZE)

        INDENT = 5
        ax.set_xlim(self.minXY().x - INDENT, self.maxXY().x + INDENT)
        ax.set_ylim(self.minXY().y - INDENT, self.maxXY().y + INDENT)

        # ----------   draw polygon and other   ----------

        circumscribed_rectangle = patches.Rectangle(self.minXY().to_tuple(),
                                                    self.size.x,
                                                    self.size.y,
                                                    linewidth=2,
                                                    facecolor='none',
                                                    edgecolor='black')
        ax.add_patch(circumscribed_rectangle)

        if is_draw_raster_approximation:
            matrix = self.create_rastr_approximation(h)
            move_matrix = np.full((4, 2), [self.minXY().x, self.minXY().y])
            random_color = "#" + \
                ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            random_color = 'silver'
            for i in range(matrix.shape[1]):
                for j in range(matrix.shape[0]):
                    if matrix[j][i]:
                        sqver = np.array([[i, j], [i + 1, j], [i + 1, j + 1],
                                          [i, j + 1]]) * h + move_matrix
                        polygon = patches.Polygon(sqver,
                                                  linewidth=1,
                                                  facecolor=random_color,
                                                  edgecolor='black',
                                                  alpha=0.33)
                        ax.add_patch(polygon)

        polygon = patches.Polygon(self.points_to_list(),
                                  linewidth=1,
                                  edgecolor='red',
                                  fill=False)
        ax.add_patch(polygon)

        exp_polygon = patches.Polygon(
            self.expand_polygon(indent_expand_polygon).points_to_list(),
            linewidth=1,
            edgecolor='green',
            fill=False)
        ax.add_patch(exp_polygon)

        bar = self.calc_centroid()
        plt.plot(bar.x, bar.y,  'co')
        plt.show()


if __name__ == '__main__':
    pol2 = Polygon([
        Vector(2, 2),
        Vector(1, 1),
        Vector(-4, 2),
        Vector(5, 13),
        Vector(4.00012, 4),
        Vector(4.00006, 4),
        Vector(4, 4)
    ])

    print(type(pol2))
    print(Polygon)
    print(type(pol2) == Polygon)
    # pol2.draw(is_draw_raster_approximation=True, h=0.5002 / 1.5)

    list_points = [[592.205, 683.901], [593.992, 680.914], [594.958, 680.656],
                   [596.495, 679.457], [596.705, 677.52], [577.463, 644.192],
                   [575.68, 643.405], [573.874, 644.137], [573.167, 644.845],
                   [569.687, 644.898], [538.79, 627.06], [537.097, 624.02],
                   [537.356, 623.054], [537.087, 621.123], [535.514, 619.973],
                   [497.03, 619.973], [495.457, 621.123], [495.188, 623.053],
                   [495.447, 624.02], [493.754, 627.06], [462.857, 644.898],
                   [459.377, 644.844], [458.67, 644.138], [456.864, 643.405],
                   [455.081, 644.192], [435.839, 677.52], [436.049, 679.457],
                   [437.586, 680.655], [438.553, 680.915], [440.339, 683.901],
                   [440.339, 719.577], [438.553, 722.564], [437.586, 722.824],
                   [436.049, 724.021], [435.839, 725.959], [455.081, 759.286],
                   [456.864, 760.073], [458.67, 759.341], [459.377, 758.634],
                   [462.857, 758.58], [493.754, 776.418], [495.447, 779.459],
                   [495.188, 780.426], [495.457, 782.355], [497.03, 783.506],
                   [535.514, 783.506], [537.087, 782.355], [537.356, 780.425],
                   [537.097, 779.459], [538.79, 776.418], [569.687, 758.58],
                   [573.167, 758.634], [573.874, 759.342], [575.68, 760.073],
                   [577.463, 759.286], [596.705, 725.959], [596.495, 724.021],
                   [594.958, 722.823], [593.992, 722.565], [592.205, 719.577],
                   [592.205, 683.9]]
