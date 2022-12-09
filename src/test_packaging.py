import sys
import time
import numpy as np
from class_nfp_packer import Nfp_Packer
from class_packing import Packing
from class_item import Item
from class_polygon import Polygon
from class_vector import Vector
from test import draw_segments_sequence
from data_rendering.items2png import items2png
# Датасеты: https://www.euro-online.org/websites/esicup/data-sets/


def packing_from_our_tests(input_file_name: str,
                           output_file_name='',
                           num_rot=4,
                           num_sort=2,
                           eps=0.0):
    """Входные данные типа test1"""
    path = "src\\input\\tests\\" + input_file_name
    f = open(path, 'r')
    num_items = int(f.readline())
    polygons = []
    list_pallet_shape = f.readline().split(' ')
    for i in range(num_items):
        list_points = f.readline().split(' ')
        points = []
        for j in range(0, len(list_points)-1, 2):
            point = Vector(float(list_points[j]), float(
                list_points[j+1]))
            points.append(point)
        if (points[0].x == points[-1].x and points[0].y == points[-1].y):
            points.pop()
        poly = Polygon(points)
        poly.sort_points()
        polygons.append(poly)
    f.close()
    pallet = Nfp_Packer(
        float(list_pallet_shape[0]), float(list_pallet_shape[1]))

    start_time = time.time()
    i = 0
    items = []
    packaging = Packing(width=float(list_pallet_shape[0]),
                        height=float(list_pallet_shape[1]),
                        drill_radius=0)

    for polygon in polygons:
        i += 1
        pallet.pack(polygon)
        items.append(Item(i, polygon.points_to_list()))
        items2png(r'C:\Users\1\Desktop\NestingProblem-BMW2022\src\output\fig' + str(i) + '.png',
                  items, packaging, False)
    print('Затраченое время:', time.time() - start_time)


def packing_from_Terashima2(input_file_name: str,
                            output_file_name: str,
                            num_rot=4,
                            num_sort=2,
                            eps=0.0):
    """Входные данные типа Terashima2 (распаковываем интересующие файлы и запускаем)"""
    # ------------  чтение файла  ------------
    path = "src\\input\\" + input_file_name
    f = open(path, 'r')
    num_items = int(f.readline())
    polygons = np.full(num_items, None)
    list_pallet_shape = f.readline().split(' ')
    for i in range(num_items):
        list_points = f.readline().split(' ')
        points = []
        for j in range(2, len(list_points) - 1, 2):
            point = [float(list_points[j]), float(list_points[j + 1])]
            points.append(point)
        if (points[0][0] == points[-1][0] and points[0][1] == points[-1][1]):
            points.pop()
        polygons[i] = np.array(points)
    f.close()
    # ------------  Упаковка  ------------
    packaging = Packing(width=float(list_pallet_shape[1]),
                        height=float(list_pallet_shape[2]),
                        drill_radius=0,
                        border_distance=0)
    packaging.polygons = polygons
    packaging.num_items = num_items
    packaging.items = np.full(packaging.num_items, None)
    for id in range(packaging.num_items):
        item = Item(id, polygons[id])
        packaging.items[id] = item

    packaging.make_items(h=eps, num_rout=num_rot)
    packaging.sort_items(num_sort=num_sort)
    packaging.greedy_packing()
    packaging.print_stats()
    packaging.change_position()
    packaging.save_pallets_in_files(output_file_name)
    return packaging.get_stats()


def packing_from_swim(input_file_name: str,
                      output_file_name: str,
                      width=5000,
                      height=10000,
                      num_rot=4,
                      num_sort=2,
                      eps=0.0):
    """Входные данные типа swim.txt (trousers.txt)"""
    # ------------  чтение файла  ------------
    path = "src\\input\\" + input_file_name
    f = open(path, 'r')
    line = f.readline()
    polygons = []
    while line:
        f.readline()  # QUANTITY
        quantity = int(f.readline().split(' ')[0][:-1])
        f.readline()  # NUMBER OF VERTICES
        num_verties = int(f.readline().split(' ')[0][:-1])
        f.readline()  # VERTICES (X,Y)
        polygon = []
        for _ in range(num_verties):
            line = f.readline()
            list_point = (''.join([
                line[i] for i in range(len(line) - 1)
                if not ((line[i] == ' ') and (line[i + 1] == ' '))
            ])).split(' ')
            point = [float(list_point[-2]), float(list_point[-1])]
            polygon.append(point)
        for _ in range(quantity):
            polygons.append(polygon)
        f.readline()  #
        line = f.readline()  # PIECE k
    f.close()
    # ------------  Упаковка  ------------
    pallet = Nfp_Packer(
        float(5000), float(10000))

    start_time = time.time()
    i = 0
    items = []
    packaging = Packing(width=5000,
                        height=float(10000),
                        drill_radius=0)

    for polygon in polygons:
        i += 1
        pallet.pack(polygon)
        items.append(Item(i, polygon.points_to_list()))
        # items2png(r'C:\Users\1\Desktop\NestingProblem-BMW2022\src\output\fig' + str(i)+'.png',
        #          items, packaging, False)
    print('Затраченое время:', time.time() - start_time)


if __name__ == '__main__':
    # for i in range(0, 1):
    #     packing_from_our_tests(input_file_name='test'+str(i)+'.txt')
    packing_from_our_tests(input_file_name='test'+str(30)+'.txt')
