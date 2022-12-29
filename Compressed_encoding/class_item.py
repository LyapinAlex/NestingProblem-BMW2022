import math
import numpy as np
from matplotlib import pyplot as plt

import data_rendering.primitives as pr
from class_polygon import Polygon
from class_vector import Vector
from check_item import check_item
from fit_item import fit_item


class Position:

    def __init__(self, pallet: 'Rectangular_pallet',
                 compressed_encoding: 'Compressed_encoding',
                 raster_coord: Vector):
        self.pallet = pallet
        self.compressed_encoding = compressed_encoding
        self.raster_coord = raster_coord

    def __str__(self):
        output = 'pallet_id: ' + str(self.pallet.id)
        output += '\nvector_coord: ' + str(self.vector_coord)
        output += '\nrotation: ' + str(self.rotation)
        return output

    def copy(self):
        copy_position = Position(self.compressed_encoding)
        copy_position.pallet = self.pallet
        copy_position.raster_coord = self.raster_coord.copy()
        return copy_position

    @property
    def vector_coord(self) -> Vector:
        return self.raster_coord * self.compressed_encoding.raster_approx.eps + self.compressed_encoding.surf_vector

    @property
    def rotation(self):
        return self.compressed_encoding.rotation


class Compressed_encoding:

    def __init__(self,
                 raster_approx: 'Raster_approximation',
                 turn: int,
                 reflection=False):
        self.raster_approx = raster_approx
        self.rotation = raster_approx.rotation + turn * math.pi / 2  # в радианах
        self.reflection = reflection  # отражено ли это приближение

        self.polygon: Polygon
        self.surf_vector: Vector
        self.compressed_encoding: np.ndarray
        self._length: int

        if not reflection:
            self._create_polygon_and_other(raster_approx, turn)
        else:
            self._create_reflection_polygon_and_other(raster_approx, turn)

        # можно за один проход считать, но думаю будет не очень читабельный код
        # ещё можно копировать, а не считать каждый раз

        self._length = self._calc_length()
        self.line_check_order = self._calc_check_order()
        self.max_holes_in_line = self._calc_max_holes()
        self.total_length_per_line = self._calc_total_length()

    def __str__(self):
        str_matrix = ""
        for num_line in range(self.compressed_encoding.shape[0] - 1, -1, -1):
            for unite in self.compressed_encoding[num_line]:
                str_matrix += str(unite) + ' '
            str_matrix += '\n'
        return str_matrix

    def __len__(self):
        return self._length

    @property
    def vertical_length(self):
        return self.compressed_encoding.shape[0]

    @property
    def horizontal_length(self):
        return self._length

    @property
    def dimensions(self):
        return Vector(self.horizontal_length, self.vertical_length)

    def __getitem__(self, key):
        return self.compressed_encoding[key]

    def _create_polygon_and_other(self, raster_approx: 'Raster_approximation',
                                  turn: int) -> None:
        self.surf_vector = Vector(
            raster_approx.matrix.shape[0],
            raster_approx.matrix.shape[1]) * raster_approx.eps
        if turn == 0:
            self.compressed_encoding = self._create_compressed_encoding(turn)
            self.surf_vector = Vector(0, 0)
        elif turn == 1:
            self.compressed_encoding = self._create_compressed_encoding(turn)
            self.surf_vector.y = 0
        elif turn == 2:
            self.compressed_encoding = self._axial_symmetry_y(
                self._axial_symmetry_x(raster_approx[0].compressed_encoding))
            self.surf_vector.axial_symmetry()
        elif turn == 3:
            self.compressed_encoding = self._axial_symmetry_y(
                self._axial_symmetry_x(raster_approx[1].compressed_encoding))
            self.surf_vector.x = 0
        self.polygon = raster_approx.polygon.copy().rotate(turn * math.pi / 2)
        self.polygon = self.polygon.move(self.surf_vector)
        self.surf_vector -= self.polygon.resize()
        if self.surf_vector.x < 0: self.surf_vector.x = 0
        if self.surf_vector.y < 0: self.surf_vector.y = 0

    def _create_reflection_polygon_and_other(self, raster_approx: 'Raster_approximation', turn: int) -> None:
        if turn == 2 and len(raster_approx.compressed_encodings) == 3:
            self.polygon = raster_approx[1].polygon.copy()
            self.compressed_encoding = self._axial_symmetry_x(
                raster_approx[1].compressed_encoding)
        else:
            self.polygon = raster_approx[turn].polygon.copy()
            self.compressed_encoding = self._axial_symmetry_x(
                raster_approx[turn].compressed_encoding)
        self.polygon.axial_symmetry_y()

        self._length = self._calc_length()
        self.polygon = self.polygon.move(
            Vector(self.horizontal_length, 0) * raster_approx.eps)

        self.surf_vector = self.polygon.minXY()
        if self.surf_vector.x < 0: self.surf_vector.x = 0
        if self.surf_vector.y < 0: self.surf_vector.y = 0

    def _create_compressed_encoding(self, turn: int) -> np.ndarray:
        matrix = self.raster_approx.matrix
        if turn == 0:
            line_code = np.full(matrix.shape[0], None, dtype=list)
            for j in range(0, matrix.shape[0]):
                pred = matrix[j][0]
                sum = 1
                line = []
                for i in range(1, matrix.shape[1]):
                    if matrix[j][i] == pred:
                        sum += 1
                    else:
                        if not pred: sum *= -1
                        line.append(sum)
                        pred = matrix[j][i]
                        sum = 1
                if not pred: sum *= -1
                line.append(sum)
                line_code[j] = line
        elif turn == 1:
            line_code = np.full(matrix.shape[1], None, dtype=list)
            for j in range(0, matrix.shape[1]):
                pred = matrix[matrix.shape[0] - 1][j]
                sum = 1
                line = []
                for i in range(matrix.shape[0] - 2, -1, -1):
                    if matrix[i][j] == pred:
                        sum += 1
                    else:
                        if not pred: sum *= -1
                        line.append(sum)
                        pred = matrix[i][j]
                        sum = 1
                if not pred: sum *= -1
                line.append(sum)
                line_code[j] = line
        else:
            raise Exception("Неверно задан поворот")
        return line_code

    def _axial_symmetry_x(self, original_comp_enc: np.ndarray) -> np.ndarray:
        line_code = np.full(original_comp_enc.shape[0], None, dtype=list)
        for num_line in range(original_comp_enc.shape[0]):
            line_code[num_line] = []
            for unite in original_comp_enc[num_line]:
                line_code[num_line].insert(0, unite)
        return line_code

    def _axial_symmetry_y(self, original_comp_enc: np.ndarray) -> np.ndarray:
        line_code = np.full(original_comp_enc.shape[0], None, dtype=list)
        for num_line in range(original_comp_enc.shape[0]):
            line_code[original_comp_enc.shape[0] - 1 - num_line] = []
            for unite in original_comp_enc[num_line]:
                line_code[original_comp_enc.shape[0] - 1 -
                          num_line].append(unite)
        return line_code

    def _calc_check_order(self) -> np.ndarray:
        line_length = self.compressed_encoding.shape[0]
        check_order = np.zeros((line_length, 2), dtype=int)

        for num_line in range(line_length):
            max_unite = -line_length
            for unite in self[num_line]:
                max_unite = max(max_unite, unite)
            check_order[num_line][0] = num_line
            check_order[num_line][1] = max_unite

        check_order = check_order[np.argsort(
            check_order[:, 1])]  # Закоментировать для замедления
        check_order = check_order[:, 0]
        check_order = np.flip(check_order)

        return check_order

    def _calc_max_holes(self) -> np.ndarray:
        line_length = self.compressed_encoding.shape[0]
        max_holes = np.zeros(line_length, dtype=int)

        for num_line in range(line_length):
            min_unite = 0
            for unite in self[num_line]:
                min_unite = min(min_unite, unite)
            max_holes[num_line] = min_unite

        return max_holes

    def _calc_total_length(self) -> np.ndarray:
        line_length = self.compressed_encoding.shape[0]
        total_length = np.zeros(line_length, dtype=int)

        for num_line in range(line_length):
            sum_unites = 0
            for unite in self[num_line]:
                if unite > 0:
                    sum_unites += unite
            total_length[num_line] = sum_unites

        return total_length

    def _calc_length(self) -> int:
        length = 0
        for unite in self[0]:
            length += abs(unite)
        return length

    def draw(self):
        polygon = self.polygon

        fig, ax = plt.subplots()
        pr.image_size(fig, polygon.size)
        pr.focusing_on_subject(ax, polygon.minXY(), polygon.maxXY())

        pr.draw_compressed_encoding(ax, polygon, self.compressed_encoding,
                                    self.raster_approx.eps, self.surf_vector)
        pr.draw_polygon(ax, polygon)

        plt.show()


class Raster_approximation:

    def __init__(self,
                 item: 'Item',
                 eps: float,
                 rotation: float,
                 is_reflectable=False,
                 num_turns=4):
        self.item = item
        self.polygon = self.item.expand_polygon.copy().rotate(
            rotation).move_to_origin()
        self.eps = eps
        self.rotation = rotation  # в радианах
        self.is_reflectable = is_reflectable  # допустимы ли для этого предмета отражения

        self.matrix = self._create_matrix()  #shape[1] - длина по оси Ox
        self.compressed_encodings: list[Compressed_encoding] = []
        self._add_compressed_encodings(num_turns)
        self.pixel_area = self._calc_pixel_area() * (self.eps**2)

    def __str__(self):
        str_matrix = ""
        for num_line in range(self.matrix.shape[0] - 1, -1, -1):
            for unite in self.matrix[num_line]:
                str_matrix += str(unite) + ' '
            str_matrix += '\n'
        return str_matrix

    def __getitem__(self, key):
        return self.compressed_encodings[key]

    def _create_matrix(self) -> np.ndarray:
        return self.polygon.create_rastr_approximation(self.eps)

    def _add_compressed_encodings(self, num_turns):
        self.compressed_encodings.append(Compressed_encoding(self, 0))
        if num_turns == 2:
            self.compressed_encodings.append(Compressed_encoding(self, 2))
        elif num_turns == 4:
            self.compressed_encodings.append(Compressed_encoding(self, 1))
            self.compressed_encodings.append(Compressed_encoding(self, 2))
            self.compressed_encodings.append(Compressed_encoding(self, 3))
        if not self.is_reflectable:
            return
        self.compressed_encodings.append(Compressed_encoding(self, 0, True))
        if num_turns == 2:
            self.compressed_encodings.append(Compressed_encoding(
                self, 2, True))
        elif num_turns == 4:
            self.compressed_encodings.append(Compressed_encoding(
                self, 1, True))
            self.compressed_encodings.append(Compressed_encoding(
                self, 2, True))
            self.compressed_encodings.append(Compressed_encoding(
                self, 3, True))

    def _calc_pixel_area(self):
        area = 0
        for line in self[0].compressed_encoding:
            for unite in line:
                if unite > 0:
                    area += unite
        return area

    def draw(self):
        fig, ax = plt.subplots()
        polygon = self.polygon

        pr.image_size(fig, polygon.size)
        pr.focusing_on_subject(ax, polygon.minXY(), polygon.maxXY())
        pr.draw_raster_approximation(ax, polygon, self.matrix, self.eps)
        pr.draw_polygon(ax, polygon)

        plt.show()


class Item:

    def __init__(self, id: int, polygon, drill_radius=0):
        if type(polygon) == Polygon:
            self.original_polygon = polygon
        else:
            self.original_polygon = Polygon(polygon)

        self.id = id
        self.position: Position
        self.expand_polygon: Polygon
        self._expand_item(drill_radius)
        self.list_raster_approx: list[Raster_approximation] = []

    def __str__(self):
        return str(self.original_polygon)

    def __getitem__(self, key):
        return self.list_raster_approx[key]

    def _expand_item(self, drill_radius=0):
        self.expand_polygon = self.original_polygon.copy().expand_polygon(
            drill_radius)
        #! добавить проверку на самопересечения
        surf_vector = self.original_polygon.minXY(
        ) - self.expand_polygon.minXY()
        self.expand_polygon.move_to_origin()
        self.original_polygon.move_to(surf_vector)

    def add_raster_approximations(self,
                                  eps=0,
                                  rotation=0.0,
                                  is_reflectable=False,
                                  num_turns=4):
        """Если is_reflectable = True, то будут добавлены так же отображения относительно оси Ox для предмета\\
        num_turns - количество поворотов на 90 градусов, для заданного поворота rotation, т.е. rotation + k*pi/2, где \\
        k = 0 при num_turns = 1\\
        k = 0, 2 при num_turns = 2\\
        k = 0, 1, 2, 3 при num_turns = 4"""
        if num_turns < 1 or num_turns > 4 or num_turns == 3:
            raise Exception("Неверно заданно число поворотов")
        self.list_raster_approx.append(
            Raster_approximation(self, eps, rotation, is_reflectable,
                                 num_turns))

    def get_original_polygon_on_position(self) -> Polygon:
        """Возвращает копию исходного предмета на своей позиции"""

        def move_polygons(poly: Polygon, exp_polygon: Polygon):
            surf_vec = poly.minXY() - exp_polygon.minXY()
            exp_polygon.move_to_origin()
            poly.move_to(surf_vec)

        polygon = self.original_polygon.copy()
        expand_polygon = self.expand_polygon.copy()

        polygon.rotate(self.position.rotation)
        expand_polygon.rotate(self.position.rotation)
        move_polygons(polygon, expand_polygon)

        compr_encoding = self.position.compressed_encoding
        if compr_encoding.reflection:
            polygon.axial_symmetry_y()
            polygon = polygon.move(
                Vector(compr_encoding.horizontal_length, 0) *
                compr_encoding.raster_approx.eps)

        polygon.move(self.position.vector_coord)
        return polygon


class Rectangular_pallet:

    def __init__(self,
                 id: int,
                 height: float,
                 width: float,
                 eps: float,
                 drill_radius=0.0,
                 border_distance=0.0):
        self.id = id
        self.eps = eps

        self.original_pallet: Polygon
        self.expand_pallet: Polygon
        self.shape: tuple[int, int]
        self._create_pallet(height, width, drill_radius, border_distance)
        self.compressed_encoding = self._create_encoding_pallet()
        self.list_plased_itemes: list[Item] = []

    def __str__(self):
        str_matrix = ""
        for num_line in range(self.shape[1] - 1, -1, -1):
            for unite in self.compressed_encoding[num_line]:
                str_matrix += str(unite) + ' '
            str_matrix += '\n'
        return str_matrix

    def __len__(self):
        return self.shape[0]

    @property
    def vertical_length(self):
        return self.shape[1]

    @property
    def horizontal_length(self):
        return self.shape[0]

    def __getitem__(self, key):
        return self.compressed_encoding[key]

    def _create_pallet(self, height, width, drill_radius, border_distance):
        indent = 0
        if border_distance > drill_radius:
            indent = border_distance - drill_radius
        self.shape = (int((width - 2 * indent) / self.eps),
                      int((height - 2 * indent) / self.eps))  # округление вниз
        self.original_pallet = Polygon([[0, 0], [0, height], [width, height],
                                        [width, 0]])
        self.original_pallet.move(Vector(-indent, -indent))
        self.expand_pallet = self.original_pallet.expand_polygon(-indent)

    def _create_encoding_pallet(self):
        compressed_encoding = np.full(self.shape[1], None)
        for i in range(self.shape[1]):
            compressed_encoding[i] = [-self.shape[0]]
        return compressed_encoding

    def _greedy_find_position(self, item_enc: Compressed_encoding):
        """Ищет возможное расположение объекта по принципу жадного алгоритма "как можно ниже, как можно левее"
        начиная с позиции positon"""
        item_shift_code = item_enc.compressed_encoding
        item_line_length = item_enc.horizontal_length
        pallet_shift_code = self.compressed_encoding
        pallet_line_length = self.horizontal_length
        positon = Vector(0, 0)

        shift = 0
        is_placed_item = False
        bad_line = 0
        while (not is_placed_item) and (positon.y + item_shift_code.shape[0] <=
                                        pallet_shift_code.shape[0]):
            while (not is_placed_item) and (
                    positon.x + shift + item_line_length <=
                    pallet_line_length):
                positon.x += shift
                is_placed_item, shift, bad_line = check_item(
                    self, item_enc, positon, bad_line)
            if not is_placed_item:
                positon.y += 1
                positon.x = 0
                shift = 0
        return is_placed_item, positon

    def _place_item(self, item_enc: Compressed_encoding, positon: Vector):
        fit_item(self.compressed_encoding, item_enc.compressed_encoding,
                 positon)

    def pack_item(self, item: Item) -> bool:
        """Размещаем верхний правый угол предмета как можно ниже, как можно левее"""
        is_placed_item = False
        best_pos = Vector(self.shape[0] + 1, self.shape[1] + 1)

        for raster_approx in item:
            for comp_encoding in raster_approx:
                is_placed_this_one, positon = self._greedy_find_position(
                    comp_encoding)
                if is_placed_this_one and positon + comp_encoding.dimensions < best_pos:
                    is_placed_item = True
                    best_pos = positon + comp_encoding.dimensions
                    placed_comp_encoding = comp_encoding

        if is_placed_item:
            item.position = Position(
                self, placed_comp_encoding,
                best_pos - placed_comp_encoding.dimensions)
            self._place_item(placed_comp_encoding,
                             best_pos - placed_comp_encoding.dimensions)
            self.list_plased_itemes.append(item)

        return is_placed_item

    def draw(self, is_draw_encoding=False):
        fig, ax = plt.subplots()
        pr.image_size(fig, self.expand_pallet.size)
        pr.focusing_on_subject(ax, self.original_pallet.minXY(),
                               self.original_pallet.maxXY())
        pr.draw_polygon(ax, self.expand_pallet, 'green')
        pr.draw_polygon(ax, self.original_pallet)
        for item in self.list_plased_itemes:
            pr.draw_polygon(ax, item.get_original_polygon_on_position(),
                            'black')
            if is_draw_encoding:
                compr_encoding = item.position.compressed_encoding
                pr.draw_compressed_encoding(ax, compr_encoding.polygon,
                                            self.compressed_encoding,
                                            compr_encoding.raster_approx.eps,
                                            compr_encoding.surf_vector)
        plt.show()


if (__name__ == '__main__'):
    eps = 0.093/2
    drill_radius = 0.2
    border_distance = 3
    height = 30
    width = 10

    pal1 = Rectangular_pallet(1, height, width, eps, drill_radius,
                              border_distance)

    it1 = Item(1, np.array([[1, 0], [0.3, 3], [3, 3.7], [2.1, 0]]), drill_radius)
    # it1 = Item(1,np.array([[0.3, 0.5], [0, 1], [0.7, 1.5], [1.2, 0.8], [3, 0.8], [3, 0.4], [1.2, 0.4], [0.6, 0.8]]), drill_radius)
    it1.add_raster_approximations(eps, math.pi / 3, False, 1)
    pal1.pack_item(it1)
    pal1.draw(True)

    it2 = Item(
        2,
        np.array([[0.3, 0.5], [0, 1], [0.7, 1.5], [1.2, 0.8], [3, 0.8],
                  [3, 0.4], [1.2, 0.4], [0.6, 0.8]]), drill_radius)
    it2.add_raster_approximations(eps, 0, True, 2)
    pal1.pack_item(it2)
    pal1.draw(True)

    it3 = Item(
        3,
        np.array([[0.3, 0.5], [0, 1], [0.7, 1.5], [1.2, 0.8], [3, 0.8],
                  [3, 0.4], [1.2, 0.4], [0.6, 0.8]]), drill_radius)
    it3.add_raster_approximations(eps, math.pi / 4, True, 4)
    pal1.pack_item(it3)
    pal1.draw(True)

    # it2 = Item(1, np.array([[0.3, 0.5], [0, 1], [0.7, 1.5], [1.2, 0.8], [3, 0.8], [3, 0.4], [1.2, 0.4], [0.6, 0.8]]), drill_radius)
    # it2.add_raster_approximations(eps, 0, True, 4)
    # for enc in it2[0]:
    #     enc.draw()
