import math
import random
import numpy as np
from math import ceil, floor
from matplotlib import patches
from matplotlib import pyplot as plt

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
        if not self.get_side(0).is_collinear(
                self.get_side(self.num_sides - 1)):
            new_points = [self.points[0]]
        else:
            new_points = []
        for i in range(1, self.num_sides):
            if not self.get_side(i).is_collinear(self.get_side(i - 1)):
                new_points.append(self.point(i))
        self.points = new_points
        self.num_sides = len(self.points)
        return

    def del_duplicate_points(self):
        _RADIUS_NEIGHBORHOOD = 0.1 # в милиметрах
        new_points = [self.points[0]]
        new_prev_point = self.points[0]
        for i in range(1, self.num_sides):
            if not abs(new_prev_point - self.point(i)) < _RADIUS_NEIGHBORHOOD:
                new_points.append(self.point(i))
                new_prev_point = self.points[i]
        if abs(new_points[0] - new_points[len(new_points)-1]) < _RADIUS_NEIGHBORHOOD:
            new_points.pop()
        self.points = new_points
        self.num_sides = len(self.points)
        return

    def bring_points2normal_appearance(self):
        """Удаляет дублирующиеся точки, потом удаляет среднюю из трёх соседствующих точек лежащих на одной прямой, 
        далее упорядочивает их так, что первой вершиной становится самая нижняя (если таких несколько, то из них самая левая), 
        дальше идут вершины против часовой стрелки"""
        self.del_duplicate_points()
        self.del_points_on_one_line()
        self.sort_points()
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
        centroid = Vector(0, 0)
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
        self_copy = self.copy()
        target_value = self_copy.area_circumscribed_rectangle()
        target_side = -1
        for j in range(self_copy.num_sides):
            self_copy.rotate_on_side(j)
            new_value = self_copy.area_circumscribed_rectangle()
            if new_value < target_value:
                target_value = new_value
                target_side = j
        if target_side != -1:
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
                    (edges[k][i] != 0)):  #если наталкнулись на угол и т.п.
                    rastr_approximation[k][i] = 1
                elif (edges[k][i] % 2 == 1):  #если наталкнулись на пересечение
                    rastr_approximation[k][i] = 1
                    if k:
                        rastr_approximation[k - 1][
                            i] = 1  # проверка на не выход за границы массива
                    flag = not flag
                if flag:  #заливка
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
        return rastr_approximation[0:n_y - 1, 0:n_x - 1]  #срез матрицы

    def create_rastr_approximation(self, h: float):
        edges = self.create_rastr_array_edges(h)
        rastr_approximation = self.rastr_painting_over_inside(edges)
        rastr_approximation = self.create_rastr_border(h, rastr_approximation)
        return rastr_approximation

# -----------------------------  Rotate and move   -----------------------------

    def rotate(self, angle):
        for point in self.points:
            point.rotate(angle)
        self.round_points()
        self.resize()
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
        plt.plot(bar.x, bar.y, 'co')
        plt.show()
