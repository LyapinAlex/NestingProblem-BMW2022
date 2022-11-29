import math
import random
import numpy as np
from matplotlib import patches
from matplotlib import pyplot as plt

from src.smth2matrix.polygon2matrix import polygon2matrix
from src.smth2matrix.polyline2matrix import polyline2matrix
from src.smth2matrix.shift2zero import shift2zero
from src.shift_code.simple2mixed_shift import simple2mixed_shift
from src.preprocess.expand_polygon import expand_polygon
from src.shift_code.classic2new_shift import classic2new_shift
from src.smth2lines.polygon2segments import polygon2segments


class Item:

    def __init__(self, id: int, points):
        self.id = id
        self.points = points
        self.area = None
        self.shell_points = None

        # ----------  Code   -----------
        self.matrix = None
        self.list_new_shift = None
        self.list_check_order = None
        self.pixel_area = None
        self.segments = None
        self.t_vector = None
        self.packed = False

        # --------  Position   ---------
        self.raster_coord = None
        self.optimal_x = None
        self.optimal_y = None
        self.rotation = 0
        self.reflection = False
        self.pallet_id = None

        # ----------  Trash   ----------
        self.list_matrix = None


    def clear_coordinat(self):
        self.raster_coord = None
        self.optimal_x = None
        self.optimal_y = None
        self.rotation = 0
        self.reflection = False
        self.pallet_id = None
        return None


    def creat_polygon_shell(self, drill_radius):
        """Создает облочку вокруг предмета с отсупом в drill_radius.
        Перемещает фигуры и ее фигуру в первую координатную четверть, сохраняя корректное расположение фигуры внутри своей оболочки.

        Инициализирует в Item атрибуты:
        shell_points - точки описывающие оболочку
        """
        x_min_pol, y_min_pol = np.amin(self.points, axis=0)
        self.shell_points = expand_polygon(self.points, drill_radius)
        x_min_shell, y_min_shell = np.amin(self.shell_points, axis=0)
        vector_surf = np.array(
            [x_min_pol - x_min_shell, y_min_pol - y_min_shell])
        shift2zero(self.shell_points)
        shift2zero(self.points)

        for point in self.points:
            point += vector_surf

        return None


    def set_matrix(self, h):
        """Приближение объекта пиксельным способом, с размером пискля - h"""
        self.matrix = polygon2matrix(self.shell_points, h)
        return None

    def list_of_new_shift_code(self, h):
        """Приближение объекта пиксельным способом (кодировкой с переходом), с размером пискля - h

        Returns:
            np.array[4]: содержит 4 поворота текущего объекта в формате кодировки с переходом (новая)
        """

        self.set_matrix(h)

        li = np.full(4, None)
        li1 = np.full(4, None)
        for i in range(0, 4):
            li[i] = classic2new_shift(np.rot90(self.matrix, i))
            li1[i] = self.check_orders_in_new_shift(li[i])
        self.list_new_shift = li
        self.list_check_order = li1

        self.culc_pixel_area(self.list_new_shift[0])
        return None

    def set_segments(self, h):
        """Приближение объекта отрезками, с размером пискля - h"""
        self.segments = polygon2segments(self.points, h)
        return None

    def list_segments_items(self, h):
        """Приближение объекта отрезками, с размером пискля - h

        Returns:
            np.array[4]: содержит 4 поворота текущего объекта в формате кодировки с переходом (новая)
        """

        self.set_matrix(h)

        li = np.full(4, None)
        li1 = np.full(4, None)
        for i in range(0, 4):
            li[i] = classic2new_shift(np.rot90(self.matrix, i))
            li1[i] = self.check_orders_in_new_shift(li[i])
        self.list_new_shift = li
        self.list_check_order = li1

        self.culc_pixel_area(self.list_new_shift[0])
        return None

    def culc_pixel_area(self, new_shift):
        self.pixel_area = 0
        for li in new_shift:
            for i in li:
                if i > 0:
                    self.pixel_area += i


    def check_orders_in_new_shift(self, new_shift):
        mat = np.zeros((new_shift.shape[0], 2), dtype=int)
        for j in range(new_shift.shape[0]):
            m_el = - self.matrix.shape[0]
            for i in new_shift[j]:
                m_el = max(i,m_el)
            mat[j][0] = j
            mat[j][1] = m_el
        mat = mat[np.argsort(mat[:,1])]
        mat = mat[:, 0]
        mat = np.flip(mat)
        return mat


    def shift2zero(self):
        """Перемещает объект в первую координатную четверть, вниз влево"""
        return shift2zero(self.shell_points)

# -----------------------------------  Trash   -----------------------------------

    def set_rectangular_matrix(self, h):
        """Приближение объекта описанным прямоугольником"""
        x_max, y_max = np.amax(self.shell_points, axis=0)
        x_min, y_min = np.amin(self.shell_points, axis=0)

        self.matrix = np.ones((math.ceil(
            (x_max - x_min) / h), math.ceil((y_max - y_min) / h)),
            dtype="int")
        return None


    def matrix_of_border(self, h):
        """Приближение границы объекта пиксельным способом, с размером пискля - h"""
        mat = polyline2matrix(self.shell_points, h)
        return mat


    def rotationMatrix(self):
        # self.rotation = math.ceil(rotate / math.pi * 90)
        # if (self.rotation % 90 == 0):
        #     self.matrix = np.rot90(self.matrix, self.rotation // 90)
        # else:
        #     print("Не прямой поворот:", self.rotation)
        self.matrix = np.rot90(self.matrix)
        return None


    def list_of_MixedShiftC_4R(self, h):  # крутит против часовой стрелки
        """
        Приближение объекта пиксельным способом (кодировкой с переходом), с размером пискля - h

        Returns:
            np.array[4]: содержит 4 поворота текущего объекта в формате кодировки с переходом
        """

        self.set_matrix(h)

        li = np.array([None, None, None, None])
        for i in range(0, 4):
            li[i] = np.rot90(simple2mixed_shift(np.rot90(self.matrix, 3 + i)))
            # li[i] = simple2mixed_shift(np.rot90(self.matrix, i ))
        self.list_matrix = li
        return None


    def draw_polygon(self, h, code_type=0):
        """
        Отрисовывает объект с его пиксельным приближением 
        code_type = 0: простая кодировка (по умолчанию)
        code_type = 1: кодировка со сдвигом
        """
        fig, ax = plt.subplots()
        MAX_SIZE = 7
        if self.matrix.shape[0] > self.matrix.shape[1]:
            fig.set_figheight(MAX_SIZE)
            fig.set_figwidth(
                MAX_SIZE * self.matrix.shape[0]/self.matrix.shape[1])
        else:
            fig.set_figheight(
                MAX_SIZE * self.matrix.shape[1]/self.matrix.shape[0])
            fig.set_figwidth(MAX_SIZE)

        pallet = patches.Rectangle(
            (0, 0), h*self.matrix.shape[1], h*self.matrix.shape[0], linewidth=2, facecolor='none', edgecolor='black')
        ax.add_patch(pallet)
        ax.set_xlim(-1, h*self.matrix.shape[1] + 1)
        ax.set_ylim(-1, h*self.matrix.shape[0] + 1)

        if not code_type:
            random_color = "#" + \
                ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for i in range(self.matrix.shape[1]):
                for j in range(self.matrix.shape[0]):
                    if self.matrix[j][i]:
                        sqver = np.array(
                            [[i, j], [i+1, j], [i+1, j+1], [i, j+1]])*h
                        polygon = patches.Polygon(
                            sqver, linewidth=1, facecolor=random_color, edgecolor='black', alpha=0.33)
                        ax.add_patch(polygon)
        else:
            max_pl = np.amax(self.list_matrix[0])
            min_otr = np.amin(self.list_matrix[0])*(-1)
            cmapin = plt.cm.get_cmap('Blues', max_pl)
            cmapout = plt.cm.get_cmap('Reds', min_otr)

            for j in range(self.list_matrix[0].shape[1]):
                for i in range(self.list_matrix[0].shape[0]):
                    if self.list_matrix[0][i][j] > 0:
                        sqver = np.array(
                            [[i, j], [i+1, j], [i+1, j+1], [i, j+1]])*h
                        polygon = patches.Polygon(
                            sqver, linewidth=1, edgecolor='black', facecolor=cmapin(self.list_matrix[0][i][j]))
                        ax.add_patch(polygon)
                    else:
                        sqver = np.array(
                            [[i, j], [i+1, j], [i+1, j+1], [i, j+1]])*h
                        polygon = patches.Polygon(sqver, linewidth=1, edgecolor='black', facecolor=cmapout(
                            self.list_matrix[0][i][j]*(-1)))
                        ax.add_patch(polygon)

        polygon = patches.Polygon(
            self.shell_points, linewidth=1, edgecolor='red', fill=False)
        ax.add_patch(polygon)
        plt.show()
        return None



if (__name__ == '__main__'):
    h = 0.0505
    eq1 = Item(1, np.array([[0.3, 0.5], [0, 1], [0.7, 1.5], [1.2, 0.8], [3, 0.8], [3, 0.4], [1.2, 0.4], [0.6, 0.8]]))
    # eq1 = Item(1, np.array([[1, 0], [0.3, 3], [3, 3.7], [2.1, 0]]))

    eq1.creat_polygon_shell(0)
    eq1.list_of_new_shift_code(h)
    eq1.draw_polygon(h)
