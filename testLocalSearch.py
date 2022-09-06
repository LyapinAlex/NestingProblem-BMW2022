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


def check_position(pal_pixel, item_pixel):
    placed = True
    shift = 1
    

    if pal_pixel == 0:
        placed = True
        shift = 1
    else:
        if item_pixel > 0:
            placed = False
            shift = pal_pixel
            
        else:
            if item_pixel in range(0, -pal_pixel, -1):
                placed = False
                shift = pal_pixel + item_pixel
                
            else:
                placed = True
                shift = 1

    return placed, shift


def check_item(pallet, itemMatrix):
    lb_x = -1
    lb_y = -1

    for i in range( len(pallet)):
        j = 0
        while j < len( pallet[0]):
            exit = False
            check = check_position(pallet[i][j], itemMatrix[0][0])

            # print(time.time() - t)
            if check[0]:

                if len(itemMatrix) + i <= len(pallet) and len(itemMatrix[0]) + j <= len(pallet[0]):

                    # располагаем объект
                    for p in range(len(itemMatrix)):

                        for k in range(len(itemMatrix[0])):

                            # решаем есть ли пересечение
                            if pallet[i+p][j+k] > 0:

                                if itemMatrix[p][k] > 0:
                                    exit = True
                                    break
                        if exit:
                            break
                else:
                    exit = True

                # если пересечений нет и элемент влезает, то добавляем его
                if not exit:
                    lb_x = i
                    lb_y = j    
                    break

            else:
                exit = True
            j+=check[1]
                
        if not exit:
            break

    return exit, lb_x, lb_y  


def fit_item(pallet, itemMatrix, i, j):

    for p in range(len(itemMatrix)):

        k = 0
        while k < len(itemMatrix[0]):

            if  itemMatrix[p][k] > 0:
                pallet[i+p][j+k] += itemMatrix[p][k]
                k+=1
            else:
                k-= itemMatrix[p][k]
    
    return None


def fit_item_all_route(pallet, item):
    list_matrix = item.list_matrix 
    
    bounder_y = pallet.shape[1]
    bounder_x = pallet.shape[0]
    
    rout = 0
    exit = True
    # r = 0
    for r in range(4):  
        sol = check_item(pallet,  list_matrix[r])
        if sol[0] == False and ((sol[1] + len(list_matrix[r]) < bounder_x) or (sol[1] + len(list_matrix[r]) < bounder_x  and sol[2] < bounder_y)):
            item.lb_x = sol[1]
            item.lb_y = sol[2]
            item.rotation = r * math.pi / 2
            exit = False
            bounder_x = sol[1]  + len(list_matrix[r])
            bounder_y = sol[2]  
            rout = r

    if not exit:
        fit_item(pallet, list_matrix[rout], item.lb_x, item.lb_y )
  
    return pallet, exit

def find_lb_coordinates(items, eps):
    for item in items:
        item.lb_x = item.lb_x * eps
        item.lb_y = item.lb_y * eps
    return items


# # для того что бы убрать поворот, замени метод fit_item_all_route  на fit_item
def fit_pallets(matrix_shape, items, eps):
    
    pallets = []
    pallets.append(np.zeros(matrix_shape, dtype = np.uint16))
    for item in items:
 
        i=0
        exit = True
        while exit and i<len(pallets):
            # print(pallets[i].rot90(), i )
           
            pallets[i], exit = fit_item_all_route(pallets[i], item)
            if exit and i==(len(pallets)-1):

                pallets.append(np.zeros(matrix_shape, dtype = np.uint16))
            if not exit:
                
                item.pallet_number = i
            i+=1
    
    find_lb_coordinates(items, eps)
    return pallets


def swap(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


def locSearch(matrix_shape , poligons, eps):

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
    eps = 5
    pallet_width = 20
    pallet_height = 20
    numPoligons = 10

    pal = pallet.Pallet(0, pallet_width, pallet_height, eps)
    g = generate.Generator(pallet_width, pallet_height, numPoligons )
    items = g.start(eps)

    t = time.time()

    print(locSearch(pal.shape , items, eps))

    print(time.time() - t)