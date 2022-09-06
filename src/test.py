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
    while (not placed) and (abs_uk + shift + len_it < len_pal):
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
    shift = 0
    placed = False
    while (not placed) and (y + item.shape[0] <= pallet.shape[0]):
        while (not placed) and (x + shift + len_it <= len_pal):
            x += shift
            placed, shift = check_item(item, len_it, pallet, x, y)
        if not placed:
            y += 1
            x = 0
            shift = 0
    return placed, x, y


def main():
    pallet = [4, -6, 3, -3]
    len_pal = 0
    for i in pallet:
        len_pal += abs(i)

    item = [3, -3, 2]
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
    item[0] = [-2, -1, -3]
    item[1] = [2, -1, -2, -1]

    len_item = 0
    for i in item[0]:
        len_item += abs(i)

    placed_item, x, y = find_position(item, len_item, pal, len_pal)

    print("Итог подстановки:", placed_item, x, y)


def main2():
    pallet = [4, -6, 3, -3]
    len_pal = 0
    for i in pallet:
        len_pal += abs(i)

    item = [2, -4, 2]
    len_it = 0
    for i in item:
        len_it += abs(i)

    placed, abs_uk = check_item0(item, len_it, pallet, len_pal)

    # print("Поиск вхождения:")
    my_print(pallet)
    my_print(item, abs_uk, 0)
    # ---------
    print(placed, abs_uk)
    x_0 = abs_uk
    if placed:
        a, i_p = get_pixel(pallet, x_0)
        print(pallet[i_p], a, len(pallet), i_p)
        print(pallet[i_p] - a)

        if 0 < i_p and i_p < len(pallet):
            print("первый тип")

        elif i_p == 0 and len(pallet) != 1:
            print("второй тип")

        elif i_p == len(pallet) - 1 and len(pallet) != 1:
            print("третий тип")

        else:  #len(pallet)==1
            print("четвёртый тип")


# ---------
# print("Подстановка:")
# my_print(pallet)


def main4():
    # Начальные данные
    pallet_width = 50
    pallet_height = 50
    eps = 1

    pal = Pallet(pallet_width, pallet_height, eps)

    num_polygons = 3
    polygons = create_list_of_items(num_polygons, pallet_width, pallet_height,
                                    eps)

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
    main2()
    # li = [1,2,3]
    # print(li)
    # li.insert(1,-2)
    # print(li)
    # li.pop(0)
    # print(li)