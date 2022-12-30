import math
import time
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
        
    @property
    def item(self):
        return self.compressed_encoding.raster_approx.item
        
    @property
    def eps(self):
        return self.compressed_encoding.raster_approx.eps

    @property
    def polygon(self):
        return self.compressed_encoding.polygon

    @property
    def polygon_on_position(self):
        return self.item.get_original_polygon_on_position(self)

    @property
    def encoding(self):
        return self.compressed_encoding.compressed_encoding

    @property
    def surf_vector(self):
        return self.compressed_encoding.surf_vector


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
        self.total_length_per_line = self._calc_total_length()
        self.max_unit_in_line = self._calc_max_units()

    def __str__(self):
        str_matrix = ""
        for num_line in range(self.compressed_encoding.shape[0] - 1, -1, -1):
            for unit in self.compressed_encoding[num_line]:
                str_matrix += str(unit) + ' '
            str_matrix += '\n'
        return str_matrix

    @property
    def vertical_length(self):
        return self.compressed_encoding.shape[0]

    @property
    def horizontal_length(self):
        return self._length

    @property
    def dimensions(self):
        return Vector(self.horizontal_length, self.vertical_length)

    @property
    def eps(self):
        return self.raster_approx.eps
    
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
            for unit in original_comp_enc[num_line]:
                line_code[num_line].insert(0, unit)
        return line_code

    def _axial_symmetry_y(self, original_comp_enc: np.ndarray) -> np.ndarray:
        line_code = np.full(original_comp_enc.shape[0], None, dtype=list)
        for num_line in range(original_comp_enc.shape[0]):
            line_code[original_comp_enc.shape[0] - 1 - num_line] = []
            for unit in original_comp_enc[num_line]:
                line_code[original_comp_enc.shape[0] - 1 -
                          num_line].append(unit)
        return line_code

    def _calc_check_order(self) -> np.ndarray:
        check_order = np.zeros((self.vertical_length, 2), dtype=int)

        for num_line in range(self.vertical_length):
            max_unit = 0
            for unit in self[num_line]:
                max_unit = max(max_unit, unit)
            check_order[num_line][0] = num_line
            check_order[num_line][1] = max_unit

        check_order = check_order[np.argsort(
            check_order[:, 1])]  # Закоментировать для замедления
        check_order = check_order[:, 0]
        check_order = np.flip(check_order)

        return check_order

    def _calc_total_length(self) -> np.ndarray:
        total_length = np.zeros(self.vertical_length, dtype=int)

        for num_line in range(self.vertical_length):
            sum_units = 0
            for unit in self[num_line]:
                if unit > 0:
                    sum_units += unit
            total_length[num_line] = sum_units

        return total_length

    def _calc_max_units(self) -> np.ndarray:
        max_units = np.zeros(self.vertical_length, dtype=int)

        for num_line in range(self.vertical_length):
            max_unit = 0
            for unit in self[num_line]:
                max_unit = max(max_unit, unit)
            max_units[num_line] = max_unit

        return max_units

    def _calc_length(self) -> int:
        length = 0
        for unit in self[0]:
            length += abs(unit)
        return length

    def draw(self):
        polygon = self.polygon

        fig, ax = plt.subplots()
        pr.image_size(fig, polygon.size)
        pr.focusing_on_subject(ax, polygon.minXY(), polygon.maxXY())

        pr.draw_compressed_encoding(ax, polygon.minXY(), self.compressed_encoding, self.eps, self.surf_vector)
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
            for unit in self.matrix[num_line]:
                str_matrix += str(unit) + ' '
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
            for unit in line:
                if unit > 0:
                    area += unit
        return area

    def draw(self):
        fig, ax = plt.subplots()
        polygon = self.polygon

        pr.image_size(fig, polygon.size)
        pr.focusing_on_subject(ax, polygon.minXY(), polygon.maxXY())
        pr.draw_raster_approximation(ax, polygon.minXY(), self.matrix, self.eps)
        pr.draw_polygon(ax, polygon)

        plt.show()


class Item:

    def __init__(self, id: int, polygon, num_copies = 1, drill_radius=0):
        if type(polygon) == Polygon:
            self.original_polygon = polygon
        else:
            self.original_polygon = Polygon(polygon)

        self.id = id
        self.num_copies = num_copies
        self.list_positions: list[Position] = []
        self.expand_polygon: Polygon
        self._expand_item(drill_radius)
        self.list_raster_approx: list[Raster_approximation] = []

    def __str__(self):
        return str(self.original_polygon)

    def __len__(self):
        return len(self.list_positions)

    def __getitem__(self, key):
        return self.list_raster_approx[key]

    def _expand_item(self, drill_radius=0):
        self.expand_polygon = self.original_polygon.copy().expand_polygon(
            drill_radius)
        #! добавить проверку на самопересечения
        surf_vec = self.original_polygon.minXY(
        ) - self.expand_polygon.minXY()
        self.expand_polygon.move_to_origin()
        self.original_polygon.move_to(surf_vec)

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

    def get_original_polygon_on_position(self, position: Position) -> Polygon:
        """Возвращает копию исходного предмета на своей позиции"""

        def move_polygons(poly: Polygon, exp_polygon: Polygon):
            surf_vec = poly.minXY() - exp_polygon.minXY()
            exp_polygon.move_to_origin()
            poly.move_to(surf_vec)

        polygon = self.original_polygon.copy()
        expand_polygon = self.expand_polygon.copy()

        polygon.rotate(position.rotation)
        expand_polygon.rotate(position.rotation)
        move_polygons(polygon, expand_polygon)

        compr_encoding = position.compressed_encoding
        if compr_encoding.reflection:
            polygon.axial_symmetry_y()
            polygon = polygon.move(
                Vector(compr_encoding.horizontal_length, 0) *
                compr_encoding.raster_approx.eps)

        polygon.move(position.vector_coord)
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

        self.plased_items_positions: list[Position]
        self.free_pixels_in_line: np.ndarray
        self.min_unit_in_line: np.ndarray
        self.compressed_encoding = self._create_encoding_pallet()

    def __str__(self):
        str_matrix = ""
        for num_line in range(self.shape[1] - 1, -1, -1):
            for unit in self.compressed_encoding[num_line]:
                str_matrix += str(unit) + ' '
            str_matrix += '\n'
        return str_matrix

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

    def _create_encoding_pallet(self) -> np.ndarray:
        compressed_encoding = np.full(self.vertical_length, None)
        for i in range(self.vertical_length):
            compressed_encoding[i] = [-self.horizontal_length]

        self.plased_items_positions = []
        self.free_pixels_in_line = np.full(self.vertical_length, self.horizontal_length)
        self.min_unit_in_line = np.full(self.vertical_length, -self.horizontal_length)

        return compressed_encoding

    def _is_plased_item1(self, item_enc: Compressed_encoding, positon: Vector) -> bool:
        """Проверка на влезабельность предмета по суммарной длине каждой его строки"""
        # если использовать то добавить следующую строку в _place_item
        ### self.free_pixels_in_line[positon.y + num_line] -= item_enc.total_length_per_line[num_line]
        for num_line in item_enc.line_check_order:
            # можно убрать переменную, но будет не читабельно
            is_placed_item = self.free_pixels_in_line[positon.y + num_line] >= item_enc.total_length_per_line[num_line]
            if not is_placed_item:
                return False
        return True

    def _is_plased_item2(self, item_enc: Compressed_encoding, positon: Vector) -> bool:
        """Проверка на влезабельность предмета по максимальной дырке паллеты и не дырки предмета"""
        for num_line in item_enc.line_check_order:
            # можно убрать переменную, но будет не читабельно
            is_placed_item = (self.min_unit_in_line[positon.y + num_line] + item_enc.max_unit_in_line[num_line] <= 0)
            if not is_placed_item:
                return False
        return True

    def _greedy_find_position(self, item_enc: Compressed_encoding, start_position = Vector(0, 0)):
        """Ищет возможное расположение объекта по принципу жадного алгоритма "как можно ниже, как можно левее"
        начиная с позиции positon"""
        positon = start_position.copy()

        shift = 0
        is_placed_item = False
        bad_line = 0
        while (not is_placed_item) and (positon.y + item_enc.vertical_length <= self.vertical_length):
            if not self._is_plased_item2(item_enc, positon):
                positon.y += 1
                positon.x = 0
                shift = 0
                continue

            while (not is_placed_item) and (positon.x + item_enc.horizontal_length + shift <= self.horizontal_length):
                positon.x += shift
                is_placed_item, shift, bad_line = check_item(self, item_enc, positon, bad_line)

            if not is_placed_item:
                positon.y += 1
                positon.x = 0
                shift = 0

        return is_placed_item, positon

    def _place_item(self, item_enc: Compressed_encoding, positon: Vector):
        fit_item(self.compressed_encoding, item_enc.compressed_encoding, positon)
        for num_line in range(item_enc.vertical_length):
            min_unit = 0
            for unit in self[positon.y + num_line]:
                min_unit = min(min_unit, unit)
            
            self.min_unit_in_line[positon.y + num_line] = max(self.min_unit_in_line[positon.y + num_line], min_unit)

    def pack_item(self, item: Item) -> bool:
        """Размещаем верхний правый угол предмета как можно ниже, как можно левее"""
        is_placed_item = False
        best_pos = Vector(self.horizontal_length + 1, self.vertical_length + 1)
        start_position = Vector(0, 0)

        if len(item)>0:
            start_position = item.list_positions[-1].raster_coord.copy()
            dimensions = item.list_positions[-1].compressed_encoding.dimensions.copy()
            dimensions.x = max(dimensions.x, dimensions.y)
            dimensions.y = dimensions.x
            start_position -= dimensions
            if start_position.x<0: start_position.x=0
            if start_position.y<0: start_position.y=0

        for raster_approx in item:
            for comp_encoding in raster_approx:
                is_placed_this_one, positon = self._greedy_find_position(comp_encoding, start_position)
                if is_placed_this_one and positon + comp_encoding.dimensions < best_pos:
                    is_placed_item = True
                    best_pos = positon + comp_encoding.dimensions
                    placed_comp_encoding = comp_encoding

        if is_placed_item:
            position = Position(self, placed_comp_encoding, best_pos - placed_comp_encoding.dimensions)
            self._place_item(placed_comp_encoding, best_pos - placed_comp_encoding.dimensions)
            item.list_positions.append(position)
            self.plased_items_positions.append(position)

        return is_placed_item

    def draw(self, is_draw_encoding=False):
        fig, ax = plt.subplots()
        pr.image_size(fig, self.expand_pallet.size)
        pr.focusing_on_subject(ax, self.original_pallet.minXY(),
                               self.original_pallet.maxXY())
        pr.draw_polygon(ax, self.expand_pallet, 'green')
        pr.draw_polygon(ax, self.original_pallet)
        if is_draw_encoding:
            pr.draw_compressed_encoding(ax, self.expand_pallet.minXY(), self.compressed_encoding, self.eps, Vector(0,0))
        for position in self.plased_items_positions:
            pr.draw_polygon(ax, position.polygon_on_position, 'black')
        plt.show()


if (__name__ == '__main__'):
    eps = 0.093/4
    drill_radius = 0.1
    border_distance = 0.3
    height = 25
    width = 10

    pal1 = Rectangular_pallet(1, height, width, eps, drill_radius, border_distance)

    num1 = 10
    num2 = 20
    items : list[Item] = []

    rastering_time = time.time()
    it1 = Item(id, np.array([[1, 0], [0.3, 3], [3, 3.7], [2.1, 0]]), num1, drill_radius)
    it1.add_raster_approximations(eps, math.pi / 6, True, 4)
    items.append(it1)

    it2 = Item(id, np.array([[0.3, 0.5], [0, 1], [0.7, 1.5], [1.2, 0.8], [3, 0.8], [3, 0.4], [1.2, 0.4], [0.6, 0.8]]), num2, drill_radius)
    it2.add_raster_approximations(eps, math.pi / 3, True, 4)
    items.append(it2)

    packaging_time = time.time()

    for it in items:
        while len(it)<it.num_copies:
            pal1.pack_item(it)

    end_time = time.time()


    print("rastering_time:", packaging_time-rastering_time)
    print("packaging_time:", end_time-packaging_time)

    pal1.draw(True)

    # it = Item(id, np.array([[1, 0], [0.3, 3], [3, 3.7], [2.1, 0]]), drill_radius=drill_radius)
    # it.add_raster_approximations(eps, math.pi / 6, True, 4)
    # for rast_apr in it[0]:
    #     rast_apr.draw()
