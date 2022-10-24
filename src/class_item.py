import numpy as np

from smth2matrix.polygon2matrix import polygon2matrix
from smth2matrix.shift2zero import shift2zero
from preprocess.expand_polygon import expand_polygon
from shift_code.classic2new_shift import classic2new_shift


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

        # --------  Position   ---------
        self.raster_coord = None
        self.optimal_x = None
        self.optimal_y = None
        self.rotation = 0
        self.reflection = False
        self.pallet_id = None

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

    def culc_pixel_area(self, new_shift):
        self.pixel_area = 0
        for li in new_shift:
            for i in li:
                if i > 0:
                    self.pixel_area += i

    def check_orders_in_new_shift(self, new_shift):
        mat = np.zeros((new_shift.shape[0], 2), dtype=int)
        for j in range(new_shift.shape[0]):
            m_el = -self.matrix.shape[0]
            for i in new_shift[j]:
                m_el = max(i, m_el)
            mat[j][0] = j
            mat[j][1] = m_el
        mat = mat[np.argsort(mat[:, 1])]
        mat = mat[:, 0]
        mat = np.flip(mat)
        return mat

    def shift2zero(self):
        """Перемещает объект в первую координатную четверть, вниз влево"""
        return shift2zero(self.shell_points)
