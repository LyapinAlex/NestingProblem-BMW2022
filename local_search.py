from DrawSolution import draw_all_pallets
import generate 
import pallet
import time
import math
import numpy as np


def understand_pallets(items):
    """Разделяет объекты в массивы по номеру палет"""
    packing = []
    itemsCom = []
    for item in items:
        if item.pallet_number != None:
            itemsCom.append(item)
    usedNumPallet = max([item.pallet_number for item in  itemsCom])

    for i in range(usedNumPallet  + 1):
        packing.append([])

    for i in range(usedNumPallet  + 1):
        for item in itemsCom:
            if item.pallet_number > len(packing):
                packing.append([])
            if item.pallet_number == i:
                packing[i].append(item)
    
    return packing


def check_pixel(pal_pixel, item_pixel):
    """Если текущее расположение возможно (placed=True), возвращает то на сколько надо сдвинуться вправо (shift), 
    чтоб проверить следущий пиксель пропуская пустоты предмета
    
    Если текущее расположение невозможно (placed=False), возвращает то на сколько надо сдвинуться вправо (shift), 
    чтоб выйти за пределы заполненности
    
    Returns:
        placed, shift"""
    placed = None
    shift = None

    if item_pixel < 0:
        placed = True
        shift = -item_pixel
    elif pal_pixel == 0:
        placed = True
        shift = 1
    else:
        placed = False
        shift = pal_pixel
    return placed, shift


def check_item(pallet, item_matrix):
    """Ищет место где можно расположить объект
    
    Returns:
        placed_item, lb_x, lb_y"""
    lb_x = -1
    lb_y = -1
    placed_item = False
    i = 0
    while (i < pallet.shape[0] - item_matrix.shape[0]+1) and not placed_item:
        j = 0
        while (j < pallet.shape[1] - item_matrix.shape[1]+1) and not placed_item:
            p = 0
            placed_pixel = True
            while (p < item_matrix.shape[0]) and placed_pixel:
                k = 0
                while (k < item_matrix.shape[1]) and placed_pixel:
                    placed_pixel, shift = check_pixel(pallet[i+p][j+k], item_matrix[p][k])
                    k+=shift
                p+=1
            if placed_pixel: 
                placed_item = True
                lb_x = i
                lb_y = j 
            j+=1
        i+=1
    return placed_item, lb_x, lb_y


def fit_item(pallet, item_matrix, i, j):
    """Располагает предмет на палете"""
    for p in range(item_matrix.shape[0]):
        k = 0
        while k < item_matrix.shape[1]:
            if  item_matrix[p][k] > 0:
                pallet[i+p][j+k] += item_matrix[p][k]
                k += 1
            else:
                k -= item_matrix[p][k]
    return None


def fit_item_all_route(pallet, item):
    """Выбирает лучший поворот предмета и располагает его на палете"""
    list_matrix = item.list_matrix 
    N_x = pallet.shape[0] + 1
    N_y = pallet.shape[1] + 1
    rout = 0
    placed_item = False
    # r = 0
    for r in range(4):  
        sol = check_item(pallet,  list_matrix[r])
        if sol[0] and ((sol[1] + len(list_matrix[r]) < N_x) or (sol[1] + len(list_matrix[r]) < N_x  and sol[2] < N_y)):
            item.lb_x = sol[1]
            item.lb_y = sol[2]
            item.rotation = r * math.pi / 2

            N_x = sol[1]  + len(list_matrix[r])
            N_y = sol[2]  
            rout = r
            placed_item = True

    if placed_item:
        fit_item(pallet, list_matrix[rout], item.lb_x, item.lb_y)
  
    return not placed_item


def find_lb_coordinates(items, h):
    """Переводит растровые координаты в векторные"""
    for item in items:
        item.lb_x = item.lb_x * h
        item.lb_y = item.lb_y * h
    return items


# для того что бы убрать поворот, замени метод fit_item_all_route  на fit_item
def fit_pallets(matrix_shape, items, eps):
    pallets = []
    pallets.append(np.zeros(matrix_shape, dtype = np.uint16))
    for item in items:
        i=0
        exit = True
        while exit and i < len(pallets):
            exit = fit_item_all_route(pallets[i], item)
            if exit and i == (len(pallets)-1):
                pallets.append(np.zeros(matrix_shape, dtype = np.uint16))
            if not exit:
                item.pallet_number = i
            i+=1
    
    find_lb_coordinates(items, eps)
    return pallets


def swap(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


def locSearch(matrix_shape, poligons, eps):

    n = len( poligons)
    objVal = len(fit_pallets(matrix_shape,  poligons, eps))

    # print(poligons[0].lb_x)
    stop = False
    iter = 0
    while not stop:
        # print([item.id for item in poligons])
        
        t = time.time()
        betterNeighboor = (0,0)
        stop = True
        for i in range(n):

            for j in range(i + 1, n):

                for poligon in poligons:
                    poligon.clear_coordinat()

            
                pal = fit_pallets(matrix_shape, swap(poligons, i, j), eps)
                swap(poligons, i, j)
                
                val = len(pal)
                if val < objVal:
                    # print(i,j)
                    # print('best', val, 'c', i, j)
                    

                    stop = False
                    objVal = val
                    betterNeighboor = (i,j)
                    
            print(iter, ':', objVal, 't :', time.time() - t)
            iter+=1
            
        if betterNeighboor != (0,0):
            # print('1*1')
            fit_pallets(matrix_shape, swap(poligons, betterNeighboor[0], betterNeighboor[1]), eps)
            
    for poligon in poligons:
        poligon.clear_coordinat()

    fit_pallets(matrix_shape,  poligons, eps)

    draw_all_pallets(understand_pallets(poligons), pallet_width, pallet_height, eps)
    return objVal


if (__name__=='__main__'):
    eps = 1
    pallet_width = 30
    pallet_height = 20
    numPoligons = 20

    pal = pallet.Pallet(0, pallet_width, pallet_height, eps)
    g = generate.Generator(pallet_width, pallet_height, numPoligons )
    items = g.start(eps)

    t = time.time()

    # print(locSearch(pal.shape , items, eps))
    fit_pallets(pal.shape , items, eps)
    print(time.time() - t)
    draw_all_pallets(understand_pallets(items), pallet_width, pallet_height, eps)