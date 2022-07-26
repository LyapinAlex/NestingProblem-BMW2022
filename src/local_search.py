from operator import truediv
import time
import numpy as np

from greedy_alg.class_pallets import Pallets
from class_item import Item
from data_rendering.items2png import draw_all_pallets
from putting_data.create_list_of_items import create_list_of_items
from putting_data.svg2polygons import svg2polygons
from greedy_alg.fit_pallets_with_rotation import fit_pallets_with_rotation


def swap(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


def locSearch(pallet, poligons):
    objVal = len(fit_pallets_with_rotation(pallet.shape,  poligons, pallet.h))

    num_items = len(poligons)
    stop = False
    iter = 0
    while not stop:
        t = time.time()

        betterNeighboor = (0,0)
        stop = True
        for i in range(num_items - 1):
            for j in range(i + 1, num_items):
                for poligon in poligons:
                    poligon.clear_coordinat()
                pal = fit_pallets_with_rotation(pallet.shape, swap(poligons, i, j), pallet.h)
                iter+=1
                swap(poligons, i, j)
                val = len(pal)
                if val < objVal:
                    stop = False
                    objVal = val
                    betterNeighboor = (i,j)
                    
            print(iter, ':', objVal, 't :', time.time() - t)
        if betterNeighboor != (0,0):
            fit_pallets_with_rotation(pallet.shape, swap(poligons, betterNeighboor[0], betterNeighboor[1]), pallet.h)
            
    for poligon in poligons:
        poligon.clear_coordinat()

    fit_pallets_with_rotation(pallet.shape,  poligons, pallet.h)
    return objVal


def main():
    t_start = time.time()
    # Начальные данные
    pallet_width = 2000 - 2.1
    pallet_height = 1000 - 2.1
    eps = 23
    drill_radius = 2
    file_name = 'src/input/NEST001-108.svg'


    print("\nШаг сетки:", eps,"\n")
    pal = Pallets(pallet_width, pallet_height, eps)

    # num_polygons = 100
    # polygons = create_list_of_items(num_polygons, pallet_width, pallet_height, eps)
    
    [polygons, num_polygons] = svg2polygons(file_name)
    
    # print([polygons[6], np.share(polygons[6])])

    t_convert = time.time()
    print("Считано", num_polygons, "предметов за", round(t_convert - t_start, 2))
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
    # print("Использованных палет:", locSearch(pal, items))
    fit_pallets_with_rotation(pal.shape, items, eps)

    t_draw = time.time()
    print("Время работы жадного алгоритма:", round(t_draw - t_packing, 2))
    # отрисовка решения
    draw_all_pallets(items, pallet_width, pallet_height, eps, True)

    t_end = time.time()
    print("Отрисовка решения:", round(t_end - t_draw, 2))
    print()
    print(round(t_end - t_start, 6), "- общее время работы")
    return None


if (__name__=='__main__'):
    main()