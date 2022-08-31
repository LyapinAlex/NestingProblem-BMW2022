import time
import numpy as np

from class_pallet import Pallet
from class_item import Item
from data_rendering.draw_solution import draw_all_pallets
from input.create_list_of_items import create_list_of_items
from input.svg_paths2polygons import svg_paths2polygons
from greedy_algorithm.fit_pallets import fit_pallets


def swap(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


def locSearch(pallet, poligons):
    objVal = len(fit_pallets(pallet.shape,  poligons, pallet.h))

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
                pal = fit_pallets(pallet.shape, swap(poligons, i, j), pallet.h)
                iter+=1
                swap(poligons, i, j)
                val = len(pal)
                if val < objVal:
                    stop = False
                    objVal = val
                    betterNeighboor = (i,j)
                    
            print(iter, ':', objVal, 't :', time.time() - t)
        if betterNeighboor != (0,0):
            fit_pallets(pallet.shape, swap(poligons, betterNeighboor[0], betterNeighboor[1]), pallet.h)
            
    for poligon in poligons:
        poligon.clear_coordinat()

    fit_pallets(pallet.shape,  poligons, pallet.h)
    return objVal


def main1():
    pallet_width = 25
    pallet_height = 20
    num_polygons = 20
    eps = 1.5
    
    pal = Pallet(pallet_width, pallet_height, eps)

    polygons = create_list_of_items(num_polygons, pallet_width, pallet_height, eps)
    items = np.full(num_polygons, None)
    for id in range(num_polygons):
        item = Item(id, polygons[id])
        item.list_of_MixedShiftC_4R(eps)
        items[id] = item

    t = time.time()
    print("Использованных палет:", locSearch(pal, items))
    # fit_pallets(pal.shape, items, eps)
    print(time.time() - t)
    draw_all_pallets(items, pal)
    return None

def main2():
    t_start = time.time()
    pallet_width = 1000
    pallet_height = 500
    eps = 21.5
    
    pal = Pallet(pallet_width, pallet_height, eps)
    [polygons, num_polygons] = svg_paths2polygons('src/input/NEST001-108.svg')

    t_convert = time.time()
    print(round(t_convert - t_start, 6), ": cчитано", num_polygons, "предметов")
    items = np.full(num_polygons, None)
    for id in range(num_polygons):
        item = Item(id, polygons[id])
        item.list_of_MixedShiftC_4R(eps)
        items[id] = item

    t_packing = time.time()
    print(round(t_packing - t_convert, 6), ": построение растровых приближений")
    # print("Использованных палет:", locSearch(pal, items))
    fit_pallets(pal.shape, items, eps)

    t_draw = time.time()
    print(round(t_draw - t_packing, 6), ": упаковка паллеты")
    draw_all_pallets(items, pal)

    t_end = time.time()
    print(round(t_end - t_draw, 6), ": отрисовка решения")
    print()
    
    print(round(t_end - t_start, 6), ": общее время работы")
    return None


if (__name__=='__main__'):
    main2()