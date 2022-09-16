import numpy as np
import time

from data_rendering.draw_solution import draw_all_pallets
from putting_data.create_list_of_items import create_list_of_items
from putting_data.svg_paths2polygons import svg_paths2polygons
from class_item import Item
from class_pallet import Pallet
from new_greedy_alg.fit_pallets_with_rout import fit_pallets_with_rout
from old_greedy_alg.fit_pallets import fit_pallets


def old_greedy_alg(polygons, pallet_width, pallet_height, eps, drill_radius):
    pal = Pallet(pallet_width, pallet_height, eps)

    t_convert = time.time()
    # преобразование данных (создание растровых приближений)
    items = np.full(polygons.shape[0], None)
    for id in range(polygons.shape[0]):
        item = Item(id, polygons[id])
        item.creat_polygon_shell(drill_radius)
        item.list_of_MixedShiftC_4R(eps)
        items[id] = item

    # препроцессинги
    items = sorted(items, key = lambda item: - item.matrix.size)

    # алгоритм упаковки
    pallets = fit_pallets(pal.shape, items, eps)

    # вычисление высоты 
    i = np.count_nonzero(np.sum(pallets[len(pallets)-1], axis = 1))
    return items, time.time() - t_convert, i*eps, pal.shape[1]*eps


def new_greedy_alg(polygons, pallet_width, pallet_height, eps, drill_radius):
    pal = Pallet(pallet_height, pallet_width, eps)

    t_convert = time.time()
    # преобразование данных (создание растровых приближений)
    items = np.full(polygons.shape[0], None)
    for id in range(polygons.shape[0]):
        item = Item(id, polygons[id])
        item.creat_polygon_shell(drill_radius)
        item.list_of_new_shift_code(eps)
        items[id] = item

    # препроцессинги
    items = sorted(items, key = lambda item: - item.matrix.size)

    # упаковка
    pallets = fit_pallets_with_rout(pal.shape, items, eps)
    
    # вычисление высоты первой паллеты
    i = 0
    while (i<pallets[len(pallets)-1].shape[0]) and (pallets[len(pallets)-1][i][0] != -pal.shape[0]): 
        i+=1
    
    return items, time.time() - t_convert, i*eps, pal.shape[0]*eps


def main():
    # Начальные данные
    pallet_width = 2000 - 2.1
    pallet_height = 1000 - 2.1
    drill_radius = 2

    eps = 23/4
    file_name = None
    file_name = 'src/input/NEST001-108.svg'
    # file_name = 'src/input/NEST002-216.svg'
    # file_name = 'src/input/NEST003-432.svg'

    # Инициализация предметов
    if file_name == None:
        polygons = create_list_of_items(100, pallet_height, pallet_width, eps)
    else:
        polygons = svg_paths2polygons(file_name)

    # Жадный алгоритм
    print("\nШаг сетки:", eps)

    items, work_time, height, width = new_greedy_alg(polygons, pallet_width, pallet_height, eps, drill_radius)

    print("Использованная площадь:", height, "x", width)
    print("Время работы жадного алгоритма:", round(work_time, 2))
    print()
    
    # Отрисовка решения
    ann = "S = " + str(height) + " x " + str(width) + ";  time = " + str(round(work_time, 2)) + ";  Num_item = " + str(polygons.shape[0]) + ";  eps = " + str(eps)
    draw_all_pallets(items, pallet_width, pallet_height, eps, draw_pixels = False, annotations = ann)

    return None


if __name__ == '__main__':
    main()