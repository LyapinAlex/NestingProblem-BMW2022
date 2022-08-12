from DrawSolution import draw_all_pallets
from class_item import Item
import copy
from matplotlib import pyplot as plt
from matplotlib import patches
import generate 
import pallet
import time
import math
import numpy as np
import random
import unconvexpoligon as uc

from  smth2matrix.shift2zero import shift2zero 

import pdb




def draw_pallet(items, pallet_width, pallet_height):
    # fig, ax = plt.subplots(figsize=(pallet_height, pallet_height))
    fig, ax = plt.subplots()
    pallet = patches.Rectangle((0, 0), pallet_width, pallet_height, linewidth=2, facecolor='none', edgecolor='blue')
    ax.add_patch(pallet)
    ax.set_xlim(-1, pallet_width + 1)
    ax.set_ylim(-1, pallet_height + 1)
    for item in items:
        for point in item.points:
            point0_copy = point[0]
            point[0] = math.cos(item.rotation)*point[0] - math.sin(item.rotation)*point[1]
            point[1] = math.sin(item.rotation)*point0_copy + math.cos(item.rotation)*point[1]
        item.surfPoint()
        for point in item.points:
            point[0] += item.lb_x
            point[1] += item.lb_y
        polygon = patches.Polygon(item.points)
        ax.add_patch(polygon)
    return fig, ax

def print_matrix(matrix):
    for i in range(len(matrix)):
        print(matrix[i])
        print('\n')


eps = 1
pallet_width = 10
pallet_height = 10
numPoligons = 20

def getItems(number, e):
    data = []
    for id in range(number):
            # t = time.time()
                
        points = np.array(uc.arpol(uc.getPolygon(), 0.0, 1, 3))
        size = shift2zero(points)

        x = random.uniform(e, pallet_width)
        y = random.uniform(e, pallet_height)
        x/=2
        y/=2
        for point in points:

            point[0]*=(x /size[0])
            point[1]*=(y /size[1])

        item = Item(id, points)
        item.list_of_MixedShiftC_4R(e)
        data.append(item)
        # print(item.matrix)
        # for r in range(4):
            # print(item.listMatrix[r])
        # print( time.time() - t)
        # print(shift2zero(points))
    return data
            



pal = pallet.Pallet(0, pallet_width, pallet_height, eps)


def understand_pallets(items):
    packing = []
    usedNumPallet = max([item.pallet_number for item in items])

    for i in range(usedNumPallet  + 1):
        # print(i)
        packing.append([])

    for i in range(usedNumPallet  + 1):
        for item in items:
            if item.pallet_number > len(packing):
                    packing.append([])
            if item.pallet_number == i:
                packing[i].append(item)
    


    return packing

def check_position(a, b):

    check = True
    surf = 1
    if a == 0:

        check = True
        surf = 1
       
    else:

        if b > 0:

            check = False
            surf = a
            
        else:

            if b in range(0, -a, -1):
                check = False
                surf = a+b
                
            else:

                check = True
                surf = 1

    return check, surf

def check_item(pallet, itemMatrix):
    lb_x = -1
    lb_y = -1

    for i in range( len(pallet)):

        j = 0
        while j < len( pallet[0]):
 
            exit = False
            check = check_position(pallet[i][j],itemMatrix[0][0]  )

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


def fit_item(pallet, itemMatrix, i, j ):

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
    listMatrix = item.listMatrix 
    
    bounder_y = pallet.shape[1]
    bounder_x = pallet.shape[0]
    
    rout = 0
    exit = True
    for r in range(4):  
        
        sol = check_item(pallet,  listMatrix[r])
        if sol[0] == False:
            if sol[1] + len(listMatrix[r]) <=  bounder_x:
                if sol[2] <  bounder_y:
                    item.lb_x = sol[1]
                    item.lb_y = sol[2]
                    item.rotation = r * math.pi / 2
                    exit = False
                    bounder_x = sol[1]  + len(listMatrix[r])
                    bounder_y = sol[2]  
                    rout = r

        
    if not exit:
        fit_item(pallet, listMatrix[rout], item.lb_x, item.lb_y )

    
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

            # draw_all_pallets(understand_pallets(items), pallet_width, pallet_height)
     
    find_lb_coordinates(items, eps)

    return pallets



items2 = getItems(10, eps)

t = time.time()
# l = np.zeros((pallet_width, pallet_height), dtype = np.uint16)
pal = fit_pallets(pal.shape, items2, eps )
# print(locSearch(pal.shape , items2, eps))
print(time.time() - t)
draw_all_pallets(understand_pallets(items2), pallet_width, pallet_height)