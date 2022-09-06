import numpy as np

from putting_data.create_list_of_items import create_list_of_items
from data_rendering.draw_solution import draw_all_pallets
from greedy_algorithm.fit_pallets import fit_pallets
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


def get_pixel(li: list, iter: int):
    """
    Returns:
        int: значение пикселя по iter
        li[i]: указатель на ячейку к которой относится iter"""
    # проверка на ошибку
    s = 0
    for i in li:
        s += abs(i)
    if (0 > iter) or (iter > s):
        raise Exception("Ошибка подачи итератора")
    # алгоритм
    r = 0
    i = -1
    sign = 1
    while (r < iter + 1):
        i += 1
        r += abs(li[i])
    if li[i] < 0: sign = -1
    return sign * (r - iter), li[i]


def check_pixel(pal_pixel, item_pixel, max_item_pixel=0):
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


def check_pos(abs_uk, Item, len_it, Pallet):
    placed = True
    shift = 0
    otn_uk = 0
    while placed and otn_uk < len_it:
        pal_r, pal_p = get_pixel(Pallet, abs_uk + otn_uk)
        it_r, it_p = get_pixel(Item, otn_uk)
        placed, shift = check_pixel(pal_r, it_r, it_p)

        # my_print(Pallet)
        # my_print(Item, abs_uk + otn_uk, otn_uk)
        # print(placed, shift, " : ", otn_uk, pal_r, it_r)

        otn_uk += shift
    return placed, shift


def create_line_code(matrix):
    line_code = np.full(matrix.shape[0], None, dtype = list)
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
    return None
    

def check_item(Item, len_it, Pallet, len_pal):
    abs_uk = 0
    shift = 0
    placed = False
    while (not placed) and (abs_uk + len_it < len_pal) :
        abs_uk += shift
        placed, shift = check_pos(abs_uk, Item, len_it, Pallet)
    return placed, abs_uk
        

def main():
    Pallet = [4, -6, 1, -1, 1, -3]
    len_pal = 0
    for i in Pallet:
        len_pal += abs(i)

    Item = [1, -1, 1, -2, 2]
    len_it = 0
    for i in Item:
        len_it += abs(i)

    placed, abs_uk = check_item(Item, len_it, Pallet, len_pal)

    my_print(Pallet)
    my_print(Item, abs_uk, 0)
    print(placed, abs_uk)

def main1():
    # Начальные данные
    pallet_width = 50
    pallet_height = 50
    eps = 1

    pal = Pallet(pallet_width, pallet_height, eps)

    num_polygons = 10
    polygons = create_list_of_items(num_polygons, pallet_width, pallet_height, eps)

    # преобразование данных (создание растровых приближений)
    items = np.full(num_polygons, None)
    for id in range(num_polygons):
        item = Item(id, polygons[id])
        item.list_of_MixedShiftC_4R(eps)
        items[id] = item

    # алгоритм упаковки
    # print("Использованных палет:", locSearch(pal, items))
    fit_pallets(pal.shape, items, eps)

    # отрисовка решения
    draw_all_pallets(items, pal)

    return None


if __name__ == '__main__':
    main1()