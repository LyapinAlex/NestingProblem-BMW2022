from math import sqrt
import numpy as np
import time
import os

# from .class_polygon import Polygon
# from .class_item import Item, Position, Rectangular_pallet
# from .data_reader.svg2polygons import svg2polygons
# from .data_reader.dxf2polygons import dxf2polygons
# from .data_reader.txt2polygons import txt2polygons
# from .data_reader.random_polygons import random_polygons

from class_polygon import Polygon
from class_item import Item, Position, Rectangular_pallet
from data_reader.svg2polygons import svg2polygons
from data_reader.dxf2polygons import dxf2polygons
from data_reader.txt2polygons import txt2polygons
from data_reader.random_polygons import random_polygons


class Packing():

    def __init__(self, input_dir="src\\input", output_dir="src\\output"):

        # -------  Directories  ------
        self.__input_dir = input_dir
        self.__output_dir = output_dir

        # ----------  Data  ----------
        self.__items: list[Item]
        self.__not_placed_items: list[Item] = []
        self.__pallets: list[Rectangular_pallet] = []

        # --  Packaging parameters  --
        self.__eps: float
        self.__pallet_height: float
        self.__pallet_width: float
        self.__drill_radius: float
        self.__border_distance: float

        # ---------  Stats   ---------
        self.time_convert_data = 0
        self.time_packing = 0
        self.time_placing_items = 0
        self.time_finding_position = 0

    # ---------------------------------  Properties   ----------------------------------

    @property
    def target_height(self):
        return self.__pallets[-1].target_height

    @property
    def num_ussed_pallets(self):
        return len(self.__pallets)

    @property
    def num_placed_items(self):
        return len(self.__items)
    
    @property
    def num_not_placed_items(self):
        return len(self.__not_placed_items)

    # -----------------------------------  Input   ------------------------------------

    def read_polygons_from_file(self, file_name: str) -> None:
        """Считывает данные из файла
        Поддерживает форматы: svg, dxf, txt"""
        path = self.__input_dir + '\\' + file_name
        if path.endswith("svg"):
            polygons = svg2polygons(path)
        elif path.endswith("dxf"):
            polygons = dxf2polygons(path)
        elif path.endswith("txt"):
            polygons = txt2polygons(path)
        else:
            raise Exception("Ошибка в названии файла")

        self.__items = []
        for id in range(polygons.shape[0]):
            polygon = Polygon(polygons[id])
            self.__items.append(Item(id, polygon))

    def set_packaging_parameters(self,
                                 pallet_height: float,
                                 pallet_width: float,
                                 drill_radius=0.0,
                                 border_distance=0.0,
                                 eps=0.0) -> None:
        self.__pallet_height = pallet_height
        self.__pallet_width = pallet_width
        self.__drill_radius = drill_radius
        self.__border_distance = border_distance
        if eps != 0:
            self.__eps = eps
        else:
            self.__eps = round(sqrt(pallet_width * pallet_height) / 50, 2) / 4

    def create_random_polygons(self, num_items: int) -> None:
        polygons = random_polygons(
            num_items,
            min(self.__pallet_height, self.__pallet_width) / 2)

        self.__items = []
        for id in range(polygons.shape[0]):
            polygon = Polygon(polygons[id])
            self.__items.append(Item(id, polygon))

    # --------------------------------  Calculations   --------------------------------

    def __append_pallet(self) -> None:
        pallet = Rectangular_pallet(self.__pallet_height, self.__pallet_width,
                                    self.__eps, self.__drill_radius,
                                    self.__border_distance)
        self.__pallets.append(pallet)

    def __make_items_raster_approx(self, is_reflectable = False, num_turns = 4) -> None:
        for item in self.__items:
            angle = item.find_best_item_turn(1)
            item.add_raster_approximations(self.__eps, angle, is_reflectable, num_turns)

    def __sort_items(self, num_sort = 1):
        """Сортировка в порядке неубывания по\\
        0 - без сортировки\\
        1 - по площади растрового приближения\\
        2 - площади фигур"""
        if num_sort == 1:
            self.__items = sorted(self.__items, key=lambda item: -item.area_of_approximation)
        elif num_sort == 2:
            self.__items = sorted(self.__items, key=lambda item: -item.expand_polygon.area)

    def greedy_paking(self, num_turns = 4, is_reflectable = False) -> None:
        self.__make_items_raster_approx(is_reflectable, num_turns)
        self.__sort_items()
        
        for item in self.__items:
            while len(item) < item.num_copies:
                is_placed_item = False
                for pallet in self.__pallets:
                    is_placed_item = pallet.pack_item(item)
                    if is_placed_item: break
                
                if not is_placed_item:
                    self.__append_pallet()
                    pallet = self.__pallets[-1]
                    is_placed_item = pallet.pack_item(item)
                
                if not is_placed_item:
                    self.__not_placed_items.append(item)

    # -----------------------------------  Output   -----------------------------------

    def draw(self, is_draw_encoding = False) -> None:
        for pallet in self.__pallets:
            pallet.draw(is_draw_encoding=is_draw_encoding)

    # -----------------------------------  Packing   -----------------------------------

    # ----------------------------------  Eristics   ----------------------------------

if (__name__ == '__main__'):
    # eps = 0.093
    drill_radius = 0
    border_distance = 0
    height = 2000
    width = 1000
    file_name = "experiment1.txt"

    pack = Packing("Compressed_encoding\\input", "Compressed_encoding\\output")
    pack.read_polygons_from_file(file_name)
    pack.set_packaging_parameters(height, width, drill_radius, border_distance)
    pack.greedy_paking(4, False)

    print(pack.target_height)
    pack.draw()
    pack.draw()