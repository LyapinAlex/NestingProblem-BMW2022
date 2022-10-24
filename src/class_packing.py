from math import sqrt
import numpy as np
import time
import os

from class_item import Item
from class_polygon import Polygon
from putting_data.create_list_of_items import create_list_of_items
from putting_data.dxf2polygons import dxf2polygons
from putting_data.svg2polygons import svg2polygons
from putting_data.txt2polygons import txt2polygons
from data_rendering.items2DXF import items2DXF
from data_rendering.items2svg import items2svg
from data_rendering.items2png import items2png
from data_rendering.items2txt import items2txt
from greedy_alg.fit_pallets_with_rotation import fit_pallets_with_rotation


class Packing():

    def __init__(self, width, height, drill_radius = 0, border_distance = 0):
        # -------  Initial data  -------
        if border_distance > drill_radius:
            width -= (border_distance-drill_radius)*2
            height -= (border_distance-drill_radius)*2
        self.pallet_width = width
        self.pallet_height = height
        self.drill_radius = drill_radius
        self.border_distance = border_distance
        self.output_dir = "src\\output"
        self.input_dir = "src\\input"

        # -----------  Data  -----------
        self.h = None  # grid step length
        self.pallet_shape = None
        self.polygons = None
        self.items = None
        self.items_split_on_pallets = None
        
        # ----------  Stats   ----------
        self.num_items = 0
        self.num_packing_items = 0

        self.total_area_polygons = 0
        self.total_pixel_area_polygons = 0

        self.num_pallets = 0
        self.target_width = 0
        self.target_height = 0

        self.time_convert_data = 0
        self.time_packing = 0
#!доделать
        self.time_placing_items = 0
#!доделать
        self.time_finding_position = 0

# -----------------------------------  Input   ------------------------------------

    def read_polygons_from_file(self, file_name):
        """Считывает многоугольники из файлов
        Поддерживает форматы: svg, dxf, txt"""
        path = self.input_dir + '\\' + file_name
        if path.endswith("svg"):
            polygons = svg2polygons(path)
        elif path.endswith("dxf"):
            polygons = dxf2polygons(path)
        elif path.endswith("txt"):
            polygons = txt2polygons(path)
        else:
            raise Exception("Ошибка в названии файла")
        self.num_items = polygons.shape[0]
        self.items = np.full(self.num_items, None)
        for id in range(self.num_items):
            item = Item(id, polygons[id])
            self.items[id] = item
        return

    def create_random_polygons(self, num_items=70):
        self.num_items = num_items
        polygons = create_list_of_items(self.num_items, self.pallet_height,
                                        self.pallet_width)
        self.items = np.full(self.num_items, None)
        for id in range(self.num_items):
            item = Item(id, polygons[id])
            self.items[id] = item
        return

# --------------------------------  Calculations   --------------------------------

    def make_items(self, h = 0.0, num_rout = 0):
        if h == 0.0:
            self.h = round(sqrt(self.pallet_width * self.pallet_height) / 50, 2) / 4
        else:
            self.h = h

        
        self.pallet_shape = (int(self.pallet_height / self.h),
                             int(self.pallet_width / self.h)
                             )  # округление вниз
        t_convert = time.time()
        for item in self.items:
            poly = Polygon(item.points)
            if num_rout != 0:
                poly.bring_points2normal_appearance()
                if num_rout == 1: # не очень
                    poly.choose_best_turn3()
                elif num_rout == 2: # не очень
                    poly.rotate_on_side(0)
                elif num_rout == 3: # неплохо
                    poly.choose_best_turn1()
                elif num_rout == 4: # пока лучший
                    poly.choose_best_turn2()
                item.points = poly.points_to_array()
            item.area = poly.area
            item.creat_polygon_shell(self.drill_radius)
            item.list_of_new_shift_code(self.h)
            self.total_area_polygons += item.area
            self.total_pixel_area_polygons += item.pixel_area
        self.time_convert_data = round(time.time() - t_convert, 3)
        return

    def sort_items(self, num_sort = 0):
        """Сортировка в порядке неубывания по\n
        0 - количеству пикселей в растровой кодировке\n
        1 - по площади растрового приближения\n
        2 - площади фигур"""
        if num_sort == 0:
            self.items = sorted(self.items, key=lambda item: -item.matrix.size)
        elif num_sort == 1:
            self.items = sorted(self.items, key=lambda item: -item.pixel_area)
        elif num_sort == 2:
            self.items = sorted(self.items, key=lambda item: -item.area)

    def greedy_packing(self):
        t_packing = time.time()
        pallets = fit_pallets_with_rotation(self.pallet_shape, self.items,
                                            self.h)
        self.time_packing = round(time.time() - t_packing, 3)
        self.num_pallets = len(pallets)
        # вычисление целевой высоты
        i = 0
        while (i < self.pallet_shape[1]) and (
                pallets[self.num_pallets - 1][i][0] != -self.pallet_shape[0]):
            i += 1

        self.num_packing_items += self.num_items #пока формально стоит
        self.target_width = round(self.pallet_shape[0] * self.h, 1)
        self.target_height = round(
            (i + self.pallet_shape[1] * (self.num_pallets - 1)) * self.h, 1)
        return

    def split_items(self):
        """Разделяет объекты в массивы по номеру палет"""

        self.items_split_on_pallets  = [[] for i in range(self.num_pallets)]
        for item in self.items: 
            if item.pallet_id != None:
                self.items_split_on_pallets [item.pallet_id].append(item)
        
        return self.items_split_on_pallets 
#!доделать
    def change_position(self):
        """Пока работает не устойчиво, поэтому не встроить в сохранение"""
        self.split_items()
        for item in self.items:
            # item.shift2zero()

            for point in item.points:
                point0_copy = point[0]
                point1_copy = point[1]

                if item.rotation == 0:
                    point[0] = point1_copy
                    point[1] = point0_copy
                elif item.rotation == 1:
                    point[0] = -point0_copy + self.h*len(item.matrix[0])
                    point[1] = point1_copy
                elif item.rotation == 2:
                    point[0] = -point1_copy + self.h*len(item.matrix)
                    point[1] = -point0_copy + self.h*len(item.matrix[0])
                elif item.rotation == 3:
                    point[0] = point0_copy
                    point[1] = -point1_copy + self.h*len(item.matrix)

            for point in item.points:
                point[0] += item.optimal_x
                point[1] += item.optimal_y

# -----------------------------------  Output   -----------------------------------

    def clear_output(self, file_extension = None):
        """Если file_extension==None, удаляет файлы с расширением png, dxf, txt"""
        if file_extension == None:
            filelist = [f for f in os.listdir(
                self.output_dir) if f.endswith(".png") or f.endswith(".dxf") or f.endswith(".txt")]
        else:
            filelist = [f for f in os.listdir(
                self.output_dir) if f.endswith(file_extension)]

        for f in filelist:
            os.remove(os.path.join(self.output_dir, f))

    def save_pallets_in_files(self, file_name, duplicate_first_point_to_end=True, draw_pixels = False):
        """Сохраняет упаковки паллет в разных файлах
        Поддерживает форматы: txt, dxf, png, svg"""
        path = self.output_dir + '\\' + file_name

        indent = 0
        if self.border_distance > self.drill_radius:
            indent = self.border_distance - self.drill_radius

        if path.endswith(".txt"):
            for i in range(self.num_pallets):
                items2txt(path, self.items_split_on_pallets[i], duplicate_first_point_to_end)
        elif path.endswith(".dxf"):
            for i in range(self.num_pallets):
                items2DXF(path, self.items_split_on_pallets[i], self.pallet_width, self.pallet_height)
        elif path.endswith(".png"):
            for i in range(self.num_pallets):
                items2png(path, self.items_split_on_pallets[i], self, indent, draw_pixels)
        elif path.endswith(".svg"):
            for i in range(self.num_pallets):
                items2svg(path, self.items_split_on_pallets[i], self, indent)
        else:
            raise Exception(
                "Программа не умеет сохранять данные в предложенном вами формате")

    def save_items_in_file(self, file_name, duplicate_first_point_to_end=True):
        """Сохраняет предметы в одном файле
        Поддерживает форматы: txt"""
        path = self.output_dir + '\\' + file_name
        if path.endswith(".txt"):
            items2txt(path, self.items, duplicate_first_point_to_end, is_in_one_file = True)
        else:
            raise Exception(
                "Программа не умеет сохранять данные в предложенном вами формате")

    def print_stats(self):
        print("\nШаг сетки:", self.h)
        print("Использованная площадь:", self.target_height, "x",
              self.target_width)
        print("Время растрирования предметов:", self.time_convert_data)
        print("Время работы жадного алгоритма:", self.time_packing, '\n')
        percent1 = self.total_area_polygons/(self.target_height*self.target_width) * 100
        print("Процент заполненной области:", round(percent1, 2))
        percent2 = self.total_pixel_area_polygons*(self.h**2)/(self.target_height*self.target_width) * 100
        print("Процент заполненной области с учётом part_distance:", round(percent2, 2), '\n')

    def get_stats(self):
        return [self.target_height, self.time_packing]

    def get_annotation(self):
        annotation = "S = " + str(self.target_height) + " x " + str(
            self.target_width) + ";  time = " + str(
                self.time_packing) + ";  Num_item = " + str(
                    self.num_packing_items) + ";  eps = " + str(self.h) + ";  part_distance = " + str(
                        self.drill_radius * 2)  + ";  border_distance = " + str(self.border_distance) 
        return annotation

# -----------------------------------  Packing   -----------------------------------

    def packing_from_file(self, input_file_name: str, output_file_name: str, num_rot = 4, num_sort = 2, eps = 0.0):
        self.read_polygons_from_file(input_file_name)
        self.make_items(h = eps, num_rout=num_rot)
        self.sort_items(num_sort=num_sort)
        self.greedy_packing()
        self.print_stats()
        self.change_position()
        self.save_pallets_in_files(output_file_name)
        return

    def packing_random_items(self, num_items: int, output_file_name: str, num_rot = 4, num_sort = 2, eps = 0.0):
        self.create_random_polygons(num_items)
        self.make_items(h = eps, num_rout=num_rot)
        self.sort_items(num_sort=num_sort)
        self.greedy_packing()
        self.print_stats()
        self.change_position()
        self.save_pallets_in_files(output_file_name)
        return