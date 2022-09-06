import time
import numpy as np

from class_pallet import Pallet
from class_item import Item
from data_rendering.draw_solution import draw_all_pallets
from generators.create_list_of_items import create_list_of_items

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


def main():
    pallet_width = 25
    pallet_height = 20
    num_polygons = 20
    eps = 0.4
    
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


if (__name__=='__main__'):
    main()