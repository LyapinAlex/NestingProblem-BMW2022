import numpy as np
import time

from data_rendering.draw_solution import draw_all_pallets
from putting_data.create_list_of_items import create_list_of_items
from putting_data.svg_paths2polygons import svg_paths2polygons
from class_item import Item
from class_pallet import Pallet
from new_greedy_alg.fit_pallets_with_rout import fit_pallets_with_rout
from old_greedy_alg.fit_pallets import fit_pallets



def old_greedy_alg(num_polygons, polygons, pallet_width, pallet_height, eps, drill_radius):
    print("\n ------ Старый жадный алгоритм ------ \n")
    pal = Pallet(pallet_width, pallet_height, eps)

    t_convert = time.time()
    # преобразование данных (создание растровых приближений)
    items = np.full(num_polygons, None)
    for id in range(num_polygons):
        item = Item(id, polygons[id])
        item.creat_polygon_shell(drill_radius)
        item.list_of_MixedShiftC_4R(eps)
        items[id] = item

    t_prep = time.time()
    print("Построение растровых приближений:", round(t_prep - t_convert, 2))
    # препроцессинги
    items = sorted(items, key = lambda item: - item.matrix.size)

    t_packing = time.time()
    print("Сортировка решения:", round(t_packing - t_prep, 2))
    # алгоритм упаковки
    pallets = fit_pallets(pal.shape, items, eps)

    # вычисление высоты 
    i = np.count_nonzero(np.sum(pallets[len(pallets)-1], axis = 1))
    print("Использованная площадь:", i*eps,"x", pal.shape[1]*eps)
    print("Упаковка:", round(time.time() - t_packing, 2))

    print("\n ------------------------------------ \n")
    return items, time.time() - t_convert, i*eps


def new_greedy_alg(num_polygons, polygons, pallet_width, pallet_height, eps, drill_radius):
    print("\n ------ Новый жадный алгоритм ------ \n")
    pal = Pallet(pallet_height, pallet_width, eps)

    t_convert = time.time()
    # преобразование данных (создание растровых приближений)
    items = np.full(num_polygons, None)
    for id in range(num_polygons):
        item = Item(id, polygons[id])
        item.creat_polygon_shell(drill_radius)
        item.list_of_new_shift_code(eps)
        items[id] = item


    t_prep = time.time()
    print("Построение растровых приближений:", round(t_prep - t_convert, 2))
    # препроцессинги
    items = sorted(items, key = lambda item: - item.matrix.size)


    t_packing = time.time()
    print("Сортировка решения:", round(t_packing - t_prep, 2))
    # упаковка
    pallets = fit_pallets_with_rout(pal.shape, items, eps)
    
    # вычисление высоты первой паллеты
    i = 0
    while i<pallets[len(pallets)-1].shape[0] and pallets[len(pallets)-1][i][0] != -pal.shape[0]: i+=1
    print("Использованная площадь:", i*eps,"x", pal.shape[0]*eps)
    print("Упаковка:", round(time.time() - t_packing, 2))

    print("\n ----------------------------------- \n")
    return items, time.time() - t_convert, i*eps


def main():
    t_start = time.time()
    # Начальные данные
    pallet_width = 2000 - 2.1
    pallet_height = 1000 - 2.1
    drill_radius = 2

    eps = 23/4
    file_name = None
    file_name = 'src/input/NEST003-432.svg'

    #Инициализация предметов
    if file_name == None:
        num_polygons = 100
        polygons = create_list_of_items(num_polygons, pallet_height, pallet_width, eps)
    else:
        [polygons, num_polygons] = svg_paths2polygons(file_name)

    print("\nШаг сетки:", eps)
    print("Считано", num_polygons, "предметов за", round(time.time() - t_start, 2))

    items, work_time, height = new_greedy_alg(num_polygons, polygons, pallet_width, pallet_height, eps, drill_radius)

    t_draw = time.time()
    # отрисовка решения
    draw_all_pallets(items, pallet_width, pallet_height, eps)

    t_end = time.time()
    print("Отрисовка решения:", round(t_end - t_draw, 2))
    print()
    print(round(t_end - t_start, 6), "- общее время работы")
    return None


if __name__ == '__main__':
    main()