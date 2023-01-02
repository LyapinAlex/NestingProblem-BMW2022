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

# можно для каждого алгоритма сделать отдельный класс, наследуемый от какого-то основного
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
        self.__time_start = time.time()
        self.total_packing_time = 0
        self.__target_height = 0

        self.time_finding_position = 0
        self.time_placing_items = 0
        self.time_convert_data = 0

    # ---------------------------------  Properties   ---------------------------------

    @property
    def target_height(self) -> float:
        return self.__pallets[-1].target_height + (self.num_ussed_pallets-1)*(self.__pallets[0].vertical_length*self.__eps)
        # return self.__target_height

    @property
    def num_ussed_pallets(self) -> int:
        return len(self.__pallets)

    @property
    def num_items(self) -> int:
        num_items = 0
        for item in self.__items:
            num_items += item.num_copies
        return num_items

    @property
    def num_placed_items(self) -> int:
        num_items = 0
        for pallet in self.__pallets:
            num_items += len(pallet.plased_items_positions)
        return num_items
    
    @property
    def num_not_placed_items(self) -> int:
        return len(self.__not_placed_items)

    #!модернезировать для одинаковых предметов
    @property
    def num_highly_packaged_item(self) -> int:
        """Возвращает номер наиболее высоко упакованного предмета на последней палете"""
        number = 0
        hi_pack_pos = self.__items[number].list_positions[0]
        for num_item in range(self.num_items):
            pos = self.__items[num_item].list_positions[0]
            is_packed_later = hi_pack_pos.pallet.id > pos.pallet.id
            is_packed_highly = (hi_pack_pos.raster_coord + hi_pack_pos.dimensions) >= (pos.raster_coord + pos.dimensions)
            if is_packed_later or is_packed_highly:
                number = num_item
                hi_pack_pos = pos
        return number

    # -----------------------------------  Input   ------------------------------------

    #!модернезировать для одинаковых предметов
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
            self.__eps = round(sqrt(pallet_width * pallet_height) / 50, 2) / 2

    #!модернезировать для одинаковых предметов
    def create_random_polygons(self, num_items: int) -> None:
        polygons = random_polygons(
            num_items,
            min(self.__pallet_height, self.__pallet_width) / 2)

        self.__items = []
        for id in range(polygons.shape[0]):
            polygon = Polygon(polygons[id])
            self.__items.append(Item(id, polygon))

    # -------------------------------  Greedy packing   -------------------------------

    def __append_pallet(self) -> None:
        pallet = Rectangular_pallet(self.num_ussed_pallets, self.__pallet_height, self.__pallet_width,
                                    self.__eps, self.__drill_radius,
                                    self.__border_distance)
        self.__pallets.append(pallet)

    def __make_items_raster_approx(self, is_reflectable = False, num_turns = 4) -> None:
        self.time_convert_data = time.time()
        
        for item in self.__items:
            angle = item.find_best_item_turn(1)
            item.add_raster_approximations(self.__eps, angle, is_reflectable, num_turns)
        
        self.time_convert_data = time.time() - self.time_convert_data

    def __sort_items(self, num_sort = 1):
        """Сортировка в порядке неубывания по\\
        0 - без сортировки\\
        1 - по площади растрового приближения\\
        2 - площади фигур"""
        if num_sort == 1:
            self.__items = sorted(self.__items, key=lambda item: -item.area_of_approximation)
        elif num_sort == 2:
            self.__items = sorted(self.__items, key=lambda item: -item.expand_polygon.area)

    def __packing(self, previous_target_height = -1) -> None:
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
                else:
                    self.__target_height = self.__pallets[-1].target_height + (self.num_ussed_pallets-1)*(self.__pallets[0].vertical_length*self.__eps)
            if (previous_target_height!=-1) and (self.__target_height > previous_target_height):
                break
        
        self.total_packing_time = time.time() - self.__time_start
        for pallet in self.__pallets:
            self.time_finding_position += pallet.time_finding_position
            self.time_placing_items += pallet.time_placing_items
    
    def greedy_packing(self, num_turns = 4, is_reflectable = False) -> None:
        self.time_finding_position = 0
        self.time_placing_items = 0

        self.__make_items_raster_approx(is_reflectable, num_turns)
        self.__sort_items()
        self.__packing()

    # --------------------------------  Local search   --------------------------------
    ### не модернезируется для одинаковых предметов (!!! Item.num_copies = 1 !!!)
    ### считывание данных в принципе написаны так, что Item.num_copies для всех предметов рано 1
    
    def __change_id_of_items_in_order(self) -> None:
        for num_item in range(self.num_items):
            self.__items[num_item].id = num_item

    def __swap_itemes(self, n: int, m: int) -> None:
        """Меняет местами два предмета в последовательности упаковываемых предметов"""
        item = self.__items[n]
        self.__items[n] = self.__items[m]
        self.__items[m] = item

    def __change_position_items_as_on_pallet(self, pallets: list[Rectangular_pallet]):
        """Очищет позиции предметов и добавляет те, что на паллетах"""
        self.__pallets = pallets
        for item in self.__items:
            item.list_positions = []
            
        for num_pallet in range(len(pallets)):
            if num_pallet == len(pallets) - 1:
                self.__target_height = max(self.__target_height, pallets[num_pallet].target_height + num_pallet*(pallets[num_pallet].vertical_length*self.__eps))
            for position in pallets[num_pallet].plased_items_positions:
                position.item.list_positions.append(position)

    def __remove_items_position(self, num_first_item: int, pallets: list[Rectangular_pallet]) -> None:
        """Убрает предметы с позиций и возвращает присваивает те, что есть на pallets"""
        self.__not_placed_items = []
        # очищаю паллеты и размещаю на них первые предметы
        num_pallets = 0
        self.__target_height = 0
        self.__pallets = []

        for pallet in pallets:
            for position in pallet.plased_items_positions:
                if position.item.id < num_first_item-1:
                    num_pallets = max(num_pallets, position.pallet.id)

        for _ in range(num_pallets+1):
            self.__append_pallet()

        for pallet in pallets:
            for position in pallet.plased_items_positions:
                if position.item.id < num_first_item-1:
                    self.__pallets[position.pallet.id]._place_item(position.compressed_encoding, position)
                    self.__pallets[position.pallet.id].plased_items_positions.append(position.copy())
        
        self.__change_position_items_as_on_pallet(self.__pallets)

    def __iteration_local_search(self, neighborhood: int) -> None:
        self.__change_id_of_items_in_order()
        best_target_height = self.target_height
        previous_pallets = self.__pallets
        new_pallets = self.__pallets
        swap_pair = (0, 0)

        for i in range(self.num_highly_packaged_item):
            for j in range(i+1, i+neighborhood):
                if j > self.num_items-1:
                    break
                self.__swap_itemes(i, j)
                self.__remove_items_position(i, previous_pallets)
                self.__packing(best_target_height)
                if best_target_height > self.target_height:
                    swap_pair = [i, j]
                    best_target_height = self.target_height
                    new_pallets = self.__pallets
                self.__swap_itemes(i, j)
                
        self.__swap_itemes(swap_pair[0], swap_pair[1])
        self.__change_position_items_as_on_pallet(new_pallets)
        
        self.total_packing_time = time.time() - self.__time_start

    def local_search(self, num_turns = 4, is_reflectable = False, max_num_iteration = 2, neighborhood = 5) -> None:
        self.time_finding_position = 0
        self.time_placing_items = 0

        self.__make_items_raster_approx(is_reflectable, num_turns)
        self.__sort_items()
        self.__packing()
        self.print_stats()

        previous_height = self.target_height + 1
        num_iteration = 0
        while self.target_height < previous_height and num_iteration < max_num_iteration:
            previous_height = self.target_height
            self.__iteration_local_search(neighborhood)
            num_iteration += 1
            print(num_iteration)
            self.print_stats()

    # -----------------------------------  Output   -----------------------------------

    def print_stats(self, is_print_all_stats = True) -> None:

        print("------------------=======  Stats  =======------------------")
        print("Общее время работы алгоритма:", self.total_packing_time)
        print("Использованно паллет:", self.num_ussed_pallets)
        print("Высота упаковки на последей паллете:", self.target_height)
        
        if is_print_all_stats:
            print("-----------------------------------------------------------")
            print("Упакованно предметов:", self.num_placed_items)
            if self.num_not_placed_items:
                print("Предметов не влезло:", self.num_not_placed_items)
            print("Время растрирования предметов:", self.time_convert_data)
            print("Время поиска позиции:", self.time_finding_position)
            print("Время размещения предметов:", self.time_placing_items)
            
            items_area = 0
            items_pixel_area = 0
            for item in self.__items:
                items_area += item.expand_polygon.area
                items_pixel_area += item.area_of_approximation
            pallet_area = 0
            pallet_pixel_area = 0
            for pallet in self.__pallets:
                pallet_area += pallet.target_area
                pallet_pixel_area += pallet.target_pixel_area
            print("Плотность заполнения:", round(items_area/pallet_area, 3))
            print("Плотность заполнения апроксимациями:", round(items_pixel_area/pallet_pixel_area, 3))
            
        # print("Процент заполненной области:", round(123.213512, 2))
        print("------------------=======================------------------")

    def draw(self, is_draw_encoding = False) -> None:
        for pallet in self.__pallets:
            pallet.draw(is_draw_encoding=is_draw_encoding)


if (__name__ == '__main__'):
    eps = 0.5
    drill_radius = 0
    border_distance = 0

    height = 1000
    width = 1000
    file_name = "experiment1.txt"

    height = 210
    width = 100
    file_name = "test0.txt"

    pack = Packing("Compressed_encoding\\input", "Compressed_encoding\\output")
    pack.read_polygons_from_file(file_name)
    pack.set_packaging_parameters(height, width, drill_radius, border_distance, eps)


    # pack.greedy_packing(4, False)
    
    pack.local_search(4, False, 2, 30)

    # pack.print_stats()
    pack.draw()