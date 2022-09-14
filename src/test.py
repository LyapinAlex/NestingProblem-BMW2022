from turtle import right
import numpy as np

from putting_data.create_list_of_items import create_list_of_items
from class_item import Item
from class_pallet import Pallet


def my_print(li: list, start=None, iter=0):
    """Созданно для однозначных чисел"""
    if start != None:
        print('   ' * start, '|')
        print('   ' * (start - iter), end='')
    for i in li:
        if i > 0:
            for j in range(i, 0, -1):
                print(' ' + str(j), end=' ')
        elif i < 0:
            for j in range(i, 0, 1):
                print(j, end=' ')
    print()


def create_line_code(matrix):
    line_code = np.full(matrix.shape[0], None, dtype=list)
    for j in range(0, matrix.shape[0]):
        pred = matrix[j][0]
        sum = 1
        line = []
        for i in range(1, matrix.shape[1]):
            if matrix[j][i] == pred:
                sum += 1
            else:
                if not pred: sum *= -1
                line.append(sum)
                pred = matrix[j][i]
                sum = 1
        if not pred: sum *= -1
        line.append(sum)
        line_code[j] = line
    return line_code


def check_item0(item, len_it, pallet, len_pal):
    abs_uk = 0
    shift = 0
    placed = False
    while (not placed) and (abs_uk + shift + len_it <= len_pal):
        abs_uk += shift
        placed, shift = check_line(abs_uk, item, len_it, pallet)

        # my_print(pallet)
        # my_print(item, abs_uk, 0)
        # print(placed, shift)
    return placed, abs_uk


def get_pixel(li: list, iter: int):
    """
    Returns:
        int: значение пикселя по iter
        i: номер ячейки к которой относится iter"""
    r = 0
    i = -1
    sign = 1
    while (r < iter + 1):
        i += 1
        r += abs(li[i])
    if li[i] < 0: sign = -1
    return sign * (r - iter), i


def check_pixel(pal_pixel: int, item_pixel: int, max_item_pixel=0):
    """Если текущее расположение возможно (placed=True), возвращает то на сколько надо сдвинуться вправо (shift), 
    чтоб проверить следущий пиксель пропуская пустоты предмета
    
    Если текущее расположение невозможно (placed=False), возвращает то на сколько надо сдвинуться вправо (shift), 
    чтоб выйти за пределы заполненности
    
    Returns:
        placed, shift"""
    placed = None
    shift = None
    if item_pixel < 0 or pal_pixel < 0:
        placed = True
        shift = -min(item_pixel, pal_pixel)
    else:
        placed = False
        shift = pal_pixel + max_item_pixel - item_pixel
    return placed, shift


def check_line(abs_uk: int, item: list, len_it: int, pallet: list):
    """Проверяем, можно ли строчку item расположить в строчке pallet, 
    по координате abs_uk
    
    Returns:
        placed_line, shift"""
    placed_line = True
    shift = 0
    otn_uk = 0
    while placed_line and otn_uk < len_it:
        pal_r, pal_i = get_pixel(pallet, abs_uk + otn_uk)
        it_r, it_i = get_pixel(item, otn_uk)
        placed_line, shift = check_pixel(pal_r, it_r, item[it_i])
        otn_uk += shift
    return placed_line, shift


def check_item(item, len_it: int, pallet, x: int, y: int):
    """Проверяем, можно ли item расположить в pallet, 
    по координатам x, y
    
    Returns:
        placed, shift"""

    placed = True
    j = 0
    while (j < item.shape[0]) and placed:
        placed, shift = check_line(x, item[j], len_it, pallet[j + y])
        j += 1
    return placed, shift


def find_position(item, len_it: int, pallet, len_pal: int, x=0, y=0):
    """Ищет возможное расположение объекта по принципу жадного алгоритма "как можно ниже, как можно левее"
    
    Returns:
        placed: bool 
        x, y: int - растровые координаты возможного расположения"""
    shift = 0
    placed = False
    while (not placed) and (y + item.shape[0] <= pallet.shape[0]):
        while (not placed) and (x + shift + len_it <= len_pal):
            x += shift
            placed, shift = check_item(item, len_it, pallet, x, y)
            # print(x, shift, len_it, len_pal)
        if not placed:
            y += 1
            x = 0
            shift = 0
    return placed, x, y


def fit_unit(pallet, item, x_0, i_it):
    """Производит подстановку положительной ячейки предмета (i_it) в отрицательную ячейку паллеты, по коодинате x_0"""
    p_p, i_p = get_pixel(pallet, x_0)
    left_r = pallet[i_p] - p_p
    right_r = p_p + item[i_it]
    
    if 0 < i_p and i_p+1 < len(pallet):
        if left_r == 0 and right_r == 0:
            # случай 1.1
            pallet[i_p - 1] += -pallet.pop(i_p)
            pallet[i_p - 1] += pallet.pop(i_p)

        elif left_r != 0 and right_r != 0:
            # случай 1.2
            pallet.insert(i_p + 1, right_r)
            pallet[i_p] = item[i_it]
            pallet.insert(i_p, left_r)

        elif left_r == 0 and right_r != 0:
            # случай 1.3
            pallet[i_p] = right_r
            pallet[i_p - 1] += item[i_it]

        else:
            # случай 1.4
            pallet[i_p] = left_r
            pallet[i_p + 1] += item[i_it]

    elif i_p == 0 and len(pallet) != 1:
        if left_r == 0 and right_r == 0:
            # случай 2.1
            pallet.pop(i_p)
            pallet[i_p] += item[i_it]

        elif left_r != 0 and right_r != 0:
            # случай 2.2 (1.2)
            pallet.insert(i_p + 1, right_r)
            pallet[i_p] = item[i_it]
            pallet.insert(i_p, left_r)

        elif left_r == 0 and right_r != 0:
            # случай 2.3 (4.3)
            pallet[i_p] = right_r
            pallet.insert(i_p, item[i_it])

        else:
            # случай 2.4 (1.4)
            pallet[i_p] = left_r
            pallet[i_p + 1] += item[i_it]

    elif i_p == len(pallet) - 1 and len(pallet) != 1:
        if left_r == 0 and right_r == 0:
            # случай 3.1
            pallet.pop(i_p)
            pallet[i_p-1] += item[i_it]


        elif left_r != 0 and right_r != 0:
            # случай 3.2 (1.2)
            pallet.insert(i_p + 1, right_r)
            pallet[i_p] = item[i_it]
            pallet.insert(i_p, left_r)

        elif left_r == 0 and right_r != 0:
            # случай 3.3 (1.3)
            pallet[i_p] = right_r
            pallet[i_p - 1] += item[i_it]

        else:
            # случай 3.4 (4.4)
            pallet[i_p] = left_r
            pallet.insert(i_p+1, item[i_it])

    elif len(pallet)==1:
        if left_r == 0 and right_r == 0:
            # случай 4.1
            pallet[i_p] *= -1

        elif left_r != 0 and right_r != 0:
            # случай 4.2 (1.2)
            pallet.insert(i_p + 1, right_r)
            pallet[i_p] = item[i_it]
            pallet.insert(i_p, left_r)

        elif left_r == 0 and right_r != 0:
            # случай 4.3
            pallet[i_p] = right_r
            pallet.insert(i_p, item[i_it])

        else:
            # случай 4.4
            pallet[i_p] = left_r
            pallet.insert(i_p+1, item[i_it])
    
    else:
        print("Ошибка заполнения паллеты/логики программы")


def fit_line(pallet, item, x_0):
    """Производит подстановку строки предмета в строку паллеты начиная с x_0 координаты строки паллеты"""
    i_it = 0
    if item[i_it]<0:
        x_0 -= item[i_it]
        i_it = 1
    
    for i in range(i_it,len(item),2):
        fit_unit(pallet, item, x_0, i)
        if i+2<len(item):
            x_0 += item[i] + abs(item[i+1])


def fit_item(pallet, item, x, y):
    """Размещает объект на паллете по координатам (x,y), без проверки на возможность размещения"""
    for i in range(item.shape[0]):
        fit_line(pallet[y+i],item[i],x)


def create_pallet(pallet_shape):
    pallet = np.full(pallet_shape[1], None)
    for i in range(pallet_shape[1]):
        pallet[i] = [-pallet_shape[0]]
    return pallet


def new_fit_pallets(pallet_shape, items, h):
    pallets = []
    pallets.append(create_pallet(pallet_shape))
    for item in items:
        x = 0
        y = 0
        i=-1
        placed_item = False
        while not placed_item and i < len(pallets) - 1:
            i+=1
            placed_item, x, y = find_position(item.new_shift, item.matrix.shape[1], pallets[i], pallet_shape[0])
            
        if not placed_item:
            pallets.append(create_pallet(pallet_shape))
            i += 1
            x = 0
            y = 0

        item.pallet_number = i
        item.raster_coord = (x, y)
        item.lb_x = y * h
        item.lb_y = x * h
        fit_item(pallets[i], item.new_shift, x, y)

    return pallets


from turtle import color
from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np
import random
import os

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

def draw_pallet(items, pallet_width, pallet_height, h, annotat = "No annotations"):
    fig, ax = plt.subplots()
    MAX_SIZE = 20
    if pallet_width > pallet_height:
        fig.set_figheight(MAX_SIZE * pallet_height/pallet_width)
        fig.set_figwidth(MAX_SIZE)
    else:
        fig.set_figheight(MAX_SIZE)
        fig.set_figwidth(MAX_SIZE * pallet_width/pallet_height)

    plt.text(0, pallet_height*1.01, annotat, fontsize=15, color = 'green')

    pallet = patches.Rectangle((0, 0), pallet_width, pallet_height, linewidth=2, facecolor='none', edgecolor='black')
    ax.add_patch(pallet)
    ax.set_xlim(-0.5, pallet_width + 2)
    ax.set_ylim(-0.5, pallet_height + 2)

    for item in items:
        for point in item.points:
            point[0] += item.lb_x
            point[1] += item.lb_y
        matrix = item.matrix
        # отрисовка растрового приближения
        random_color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        for j in range(matrix.shape[1]):
            for i in range(matrix.shape[0]):
                if matrix[i][j] > 0:
                    sqver = np.array([[i, j], [i+1, j], [i+1, j+1], [i, j+1]])*h
                    for i in range(sqver.shape[0]):
                        sqver[i][0] += item.lb_x
                        sqver[i][1] += item.lb_y
                    polygon = patches.Polygon(sqver, linewidth=1, facecolor=random_color, edgecolor='black', alpha = 0.33)
                    ax.add_patch(polygon)
        polygon = patches.Polygon(item.points, linewidth=1, edgecolor='red', fill = False)
        ax.add_patch(polygon)
        
    plt.savefig('src\output\pallet' + str(items[0].pallet_number) + '.png')
    return None

def draw_all_pallets(items, pal):
    packing = understand_pallets(items)
    # вывод текущего решения
    for i in range(len(packing)):
        draw_pallet(packing[i], pal.height, pal.width, pal.h)
    
    return None




def main0():
    pallet = [-2, 3, -3]
    len_pal = 0
    for i in pallet:
        len_pal += abs(i)

    item = [3]
    len_it = 0
    for i in item:
        len_it += abs(i)

    placed, abs_uk = check_item0(item, len_it, pallet, len_pal)

    print("Итог подстановки:")
    my_print(pallet)
    my_print(item, abs_uk, 0)
    print(placed, abs_uk)


def main1():
    pal = np.full(3, None)
    pal[0] = [-1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
    pal[1] = [-4, 1, -5]
    pal[2] = [-10]

    len_pal = 0
    for i in pal[0]:
        len_pal += abs(i)

    item = np.full(2, None)
    item[0] = [-2, 5]
    item[1] = [7]

    len_item = 0
    for i in item[0]:
        len_item += abs(i)

    placed_item, x, y = find_position(item, len_item, pal, len_pal)

    print("Итог подстановки:", placed_item, x, y)


def main2():
    pallet = [2,-3,1,-4]
    len_pal = 0
    for i in pallet:
        len_pal += abs(i)

    item = [-1,1,-1,2,-1]
    len_it = 0
    for i in item:
        len_it += abs(i)

    placed, abs_uk = check_item0(item, len_it, pallet, len_pal)

    # print("Поиск вхождения:")
    my_print(pallet)
    my_print(item, abs_uk, 0)

    # ---------------------------------------------------------------
    
    print(placed, abs_uk)
    if placed:
        fit_line(pallet, item, abs_uk)
    
    # ---------------------------------------------------------------

    my_print(pallet)
    my_print(item, abs_uk, 0)


def main3():
    pal = np.full(5, None)
    pal[0] = [-1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
    pal[1] = [-4, 1, -5]
    pal[2] = [-10]
    pal[3] = [-10]
    pal[4] = [-10]

    len_pal = 0
    for i in pal[0]:
        len_pal += abs(i)

    item = np.full(2, None)
    item[0] = [3,-1, 1]
    item[1] = [5]

    len_item = 0
    for i in item[0]:
        len_item += abs(i)
    
    # ---------------------------------------------------------------

    for i in range(0,pal.shape[0]):
        print(pal[i])

    # ---------------------------------------------------------------

    placed_item, x, y = find_position(item, len_item, pal, len_pal)
    print("Итог подстановки:", placed_item, x, y)
    
    if placed_item:
        fit_item(pal, item, x, y)
        
    for i in range(0,pal.shape[0]):
        print(pal[i])
    
    # ---------------------------------------------------------------

    placed_item, x, y = find_position(item, len_item, pal, len_pal)
    print("Итог подстановки:", placed_item, x, y)
    
    if placed_item:
        fit_item(pal, item, x, y)
        
    for i in range(0,pal.shape[0]):
        print(pal[i])
    
    # ---------------------------------------------------------------

    placed_item, x, y = find_position(item, len_item, pal, len_pal)
    print("Итог подстановки:", placed_item, x, y)
    
    if placed_item:
        fit_item(pal, item, x, y)
        
    for i in range(0,pal.shape[0]):
        print(pal[i])
    

def main4():
    # Начальные данные
    pallet_width = 30
    pallet_height = 50
    eps = 1

    pal = Pallet(pallet_width, pallet_height, eps)

    num_polygons = 50
    polygons = create_list_of_items(num_polygons, pallet_width, pallet_height, eps)

    # polygons = [np.array([[0.01950205, 1.91209608],[0.0, 0.0],[1.37037521, 2.04113187]]),
    #     np.array([[2.0647501 , 0.0],[2.02282679, 1.81566804],[0.71079648, 2.26761315],[0.39739195, 1.94988996],[0.        , 0.23347083]]),
    #     np.array([[1.74241957, 1.09714382],[3.26024357, 0.0],[4.22879563, 0.63751876],[3.42406131, 2.62739726],[3.56711314, 5.22042994],[1.7150428 , 3.21836948],[0.        , 1.19321938]]),
    #     np.array([[ 6.94255125,  0.        ],[10.92131419,  8.48771944],[ 0.        , 12.21175777]]),
    #     np.array([[2.18946478, 0.        ],[3.33738602, 6.22776785],[2.37570264, 6.99040337],[0.        , 5.35131183]]) ,
    #     np.array([[2.64398219, 4.23888636],[0.        , 4.07240617],[1.99817698, 0.        ]])]
        # np.array([[0.        , 4.16580497],[2.91281594, 0.        ],[1.19065422, 5.35907434]]) ,
        # np.array([[0.        , 0.        ],[2.70082121, 1.01370252],[0.17095205, 2.72553846]])]

    # преобразование данных (создание растровых приближений)
    items = np.full(num_polygons, None)
    for id in range(num_polygons):
        item = Item(id, polygons[id])
        item.set_matrix(eps)
        item.new_shift = create_line_code(item.matrix)
        items[id] = item

    # алгоритм упаковки
    # print("Использованных палет:", locSearch(pal, items))
    new_fit_pallets(pal.shape, items, eps)
    # отрисовка решения
    draw_all_pallets(items, pal)

    return None


def main5():
    # Начальные данные
    pallet_width = 50
    pallet_height = 50
    eps = 1

    pal = Pallet(pallet_width, pallet_height, eps)

    num_polygons = 3
    polygons = create_list_of_items(num_polygons, pallet_width, pallet_height, eps)

    # преобразование данных (создание растровых приближений)
    items = np.full(num_polygons, None)
    for id in range(num_polygons):
        item = Item(id, polygons[id])
        item.list_of_MixedShiftC_4R(eps)
        print(create_line_code(item.matrix))
        items[id] = item

    # алгоритм упаковки
    # print("Использованных палет:", locSearch(pal, items))
    fit_pallets(pal.shape, items, eps)

    # отрисовка решения
    draw_all_pallets(items, pal)

    return None


if __name__ == '__main__':
    main4()

    # li = [1,2,3]
    # print(li)
    # li.insert(1,-2)
    # print(li)
    # li.pop(0)
    # print(li)