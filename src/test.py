from turtle import right
import numpy as np
import time
import math

from putting_data.create_list_of_items import create_list_of_items
from putting_data.svg_paths2polygons import svg_paths2polygons
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


def print_item(item):
    for i in range(0,item.shape[0]):
        print(item[i])
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

###
def choosing_turn(pallet, pallet_shape, item, x=0, y=0):
    """Ищет расположение предмета для всех поворотов и выбирает лучшый из них"""
    placed_item = False
    x_b = pallet_shape[0] + 1
    y_b = pallet_shape[1] + 1
    rout = 0

    for i in range(4):
        placed_item, x_0, y_0 = find_position(item.list_new_shift[i], item.matrix.shape[(i+1)%2], pallet, pallet_shape[0], x, y)
        if placed_item and ((y_0 + item.matrix.shape[i%2] < y_b) or ((y_0 + item.matrix.shape[i%2] == y_b)  and x_0 < x_b)):
            placed_item = True
            x_b = x_0
            y_b = y_0 + item.matrix.shape[i%2]
            rout = i
    return placed_item, x_b, y_b - item.matrix.shape[rout%2], rout
###

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

###
def new_fit_pallets_with_rout(pallet_shape, items, h):
    pallets = []
    pallets.append(create_pallet(pallet_shape))
    for item in items:
        x = 0
        y = 0
        rout = 0
        i=-1
        placed_item = False
        while not placed_item and i < len(pallets) - 1:
            i+=1
            placed_item, x, y, rout = choosing_turn(pallets[i], pallet_shape, item)
            
        if not placed_item:
            pallets.append(create_pallet(pallet_shape))
            i += 1
            placed_item, x, y, rout = choosing_turn(pallets[i], pallet_shape, item)

        if not placed_item:
            print("Предмет не влазит в паллету")
        else:
            item.pallet_number = i
            item.raster_coord = (x, y)
            item.lb_x = y * h
            item.lb_y = x * h
            item.rotation = rout * math.pi / 2
            fit_item(pallets[i], item.list_new_shift[rout], x, y)
            
    # print("Использованная площадь: хз пока")
    return pallets
###

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

# def draw_all_pallets(items, pal):
#     packing = understand_pallets(items)
#     # вывод текущего решения
#     for i in range(len(packing)):
#         draw_pallet(packing[i], pal.height, pal.width, pal.h)
    
#     return None




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
    t_start = time.time()
    # Начальные данные
    pallet_width = 1000
    pallet_height = 2000
    eps = 20

    pal = Pallet(pallet_width, pallet_height, eps)

    num_polygons = 50
    polygons = create_list_of_items(num_polygons, pallet_width, pallet_height, eps)


    # преобразование данных (создание растровых приближений)
    items = np.full(num_polygons, None)
    for id in range(num_polygons):
        item = Item(id, polygons[id])
        item.set_matrix(eps)
        item.new_shift = create_line_code(item.matrix)
        items[id] = item

    # препроцессинги
    items = sorted(items, key = lambda item: - item.matrix.size)
    # алгоритм упаковки
    # print("Использованных палет:", locSearch(pal, items))
    pallets = new_fit_pallets(pal.shape, items, eps)

    # отрисовка решения
    draw_all_pallets(items, pal)

    t_end = time.time()

    print(round(t_end - t_start, 6), "- общее время работы")
    return None


def main5():
    # Начальные данные
    pallet_width = 1000
    pallet_height = 2000
    eps = 25

    pal = Pallet(pallet_width, pallet_height, eps)

    num_polygons = 50
    polygons = create_list_of_items(num_polygons, pallet_width, pallet_height, eps)

    # преобразование данных (создание растровых приближений)
    items = np.full(num_polygons, None)
    for id in range(num_polygons):
        item = Item(id, polygons[id])
        item.set_matrix(eps)
        items[id] = item

        li = np.full(4, None)
        for i in range(0, 4):
            li[i] = create_line_code(np.rot90(item.matrix, i))
        item.list_new_shift = li


    placed_item, x, y, rout = choosing_turn(create_pallet(pal.shape), pal.shape, item)

    print(item.matrix)
    print()
    print_item(item.list_new_shift[rout])
    print()

    print(placed_item, x, y, rout)
    print()

    pallets = new_fit_pallets_with_rout(pal.shape, items, eps)

    print(pallets[0])
    print()

    return None


def main6():
    t_start = time.time()
    # Начальные данные
    pallet_width = 2000
    pallet_height = 1000
    eps = 2.5
    file_name = 'src/input/NEST003-432.svg'


    print("\nШаг сетки:", eps,"\n")
    pal = Pallet(pallet_height, pallet_width, eps)

    num_polygons = 100
    polygons = create_list_of_items(num_polygons, pallet_height, pallet_width, eps)

    # [polygons, num_polygons] = svg_paths2polygons(file_name)

    t_convert = time.time()
    print("Считано", num_polygons, "предметов за", round(t_convert - t_start, 2))
    # преобразование данных (создание растровых приближений)
    items = np.full(num_polygons, None)
    for id in range(num_polygons):
        item = Item(id, polygons[id])
        item.set_matrix(eps)
        items[id] = item
        li = np.full(4, None)
        for i in range(0, 4):
            li[i] = create_line_code(np.rot90(item.matrix, i))
        item.list_new_shift = li

    t_prep = time.time()
    print("Построение растровых приближений:", round(t_prep - t_convert, 2))
    # препроцессинги
    items = sorted(items, key = lambda item: - item.matrix.size)

    t_packing = time.time()
    print("Сортировка решения:", round(t_packing - t_prep, 2))
    # алгоритм упаковки
    # print("Использованных палет:", locSearch(pal, items))
    pallets = new_fit_pallets_with_rout(pal.shape, items, eps)
    
    # вычисление высоты 
    i = 0
    while i<pallets[0].shape[0] and pallets[0][i][0] != -pal.shape[0]: i+=1
    print("Использованная площадь:", i*eps,"x", pal.shape[0]*eps)

    t_draw = time.time()
    print("Время работы жадного алгоритма:", round(t_draw - t_packing, 2))
    # отрисовка решения
    from data_rendering.draw_solution import draw_all_pallets
    draw_all_pallets(items, pallet_width, pallet_height, eps)

    t_end = time.time()
    print("Отрисовка решения:", round(t_end - t_draw, 2))
    print()
    print(round(t_end - t_start, 6), "- общее время работы")
    return None


if __name__ == '__main__':
    main6()