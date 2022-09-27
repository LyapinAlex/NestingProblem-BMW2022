from math import sqrt
import numpy as np
import time
import os

from class_item import Item
from putting_data.create_list_of_items import create_list_of_items
from putting_data.svg_paths2polygons import svg_paths2polygons
from data_rendering.items2txt import items2txt
from putting_data.dxf2polygons import dxf2polygons
from greedy_alg.fit_pallets_with_rotation import fit_pallets_with_rotation
from data_rendering.draw_solution import draw_all_pallets


class Packing():

    def __init__(self, width, height, drill_radius):
        # -------  Initial data  -------
        self.pallet_width = width
        self.pallet_height = height
        self.drill_radius = drill_radius

        # -----------  Data  -----------
        self.h = None  # grid step length
        self.pallet_shape = None
        self.polygons = None
        self.items = None

        # ----------  Stats   ----------
        self.num_items = 0
        self.num_packing_items = 0

        self.num_pallets = 0
        self.target_width = 0
        self.target_height = 0
        self.time_convert_data = 0
        self.time_packing = 0

# -----------------------------------  Input   ------------------------------------

    def read_polygons_from_file(self, path):
        if path.endswith("svg"):
            polygons = svg_paths2polygons(path)
        elif path.endswith("DXF"):
            polygons = dxf2polygons(path)
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

    def make_items(self):
        self.h = round(sqrt(self.pallet_width * self.pallet_height) / 50,
                       2) / 4
        self.pallet_shape = (int(self.pallet_height / self.h),
                             int(self.pallet_width / self.h)
                             )  # округление вниз
        t_convert = time.time()
        for item in self.items:
            item.creat_polygon_shell(self.drill_radius)
            item.list_of_new_shift_code(self.h)
        self.time_convert_data = round(time.time() - t_convert, 3)
        return

    def sort_items(self):
        """Сортировка по неубыванию"""
        self.items = sorted(self.items, key=lambda item: -item.matrix.size)

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

        self.num_packing_items += self.num_items
        self.target_width = round(self.pallet_shape[0] * self.h, 1)
        self.target_height = round(
            (i + self.pallet_shape[1] * (self.num_pallets - 1)) * self.h, 1)
        return

# -----------------------------------  Output   -----------------------------------
#!доделать
    def draw_solution(self, draw_pixels=False):
        # очистка директории от предыдущих решений
        mydir = "src\output"
        filelist = [
            f for f in os.listdir(mydir)
            if f.endswith(".png") or f.endswith(".dxf")
        ]
        for f in filelist:
            os.remove(os.path.join(mydir, f))

        draw_all_pallets(self, draw_pixels)
#!доделать
    def save_items_in_file(self, path, duplicate_first_point_to_end=True):
        if path.endswith("txt"):
            items2txt(self.items, path, duplicate_first_point_to_end)
        elif path.endswith("DXF"):
            1  #!доделать
        else:
            raise Exception(
                "Мы ещё не умеем сохранять предметы в таком формате")

    def print_stats(self):
        print("\nШаг сетки:", self.h)
        print("Использованная площадь:", self.target_height, "x",
              self.target_width)
        print("Время растрирования предметов:", self.time_convert_data)
        print("Время работы жадного алгоритма:", self.time_packing, '\n')

    def get_annotation(self):
        annotation = "S = " + str(self.target_height) + " x " + str(
            self.target_width) + ";  time = " + str(
                self.time_packing) + ";  Num_item = " + str(
                    self.num_packing_items) + ";  eps = " + str(self.h)
        return annotation
