from math import sqrt
import numpy as np
import time

from data_rendering.draw_solution import draw_all_pallets
from putting_data.create_list_of_items import create_list_of_items
from putting_data.svg_paths2polygons import svg_paths2polygons
from data_rendering.polygons2txt import polygons2txt
from data_rendering.items2txt import items2txt
from class_item import Item
from class_packing import Packing
from greedy_alg.fit_pallets_with_rotation import fit_pallets_with_rotation


def greedy_alg0(polygons, packaging):
    t_convert = time.time()
    # преобразование данных (создание растровых приближений)
    items = np.full(polygons.shape[0], None)
    for id in range(polygons.shape[0]):
        item = Item(id, polygons[id])
        item.creat_polygon_shell(packaging.drill_radius)
        item.list_of_new_shift_code(packaging.h)
        items[id] = item

    # препроцессинги
    items = sorted(items, key=lambda item: -item.matrix.size)
    # items2txt(items, path=r'src\output\items'+str(len(polygons))+'.txt')
    # упаковка
    pallets = fit_pallets_with_rotation(packaging.pallet_shape, items, packaging.h)

    # вычисление высоты первой паллеты
    i = 0
    while (i < pallets[len(pallets) - 1].shape[0]) and (
            pallets[len(pallets) - 1][i][0] != -packaging.pallet_shape[0]):
        i += 1

    return items, time.time() - t_convert, (i + packaging.pallet_shape[1] * (len(pallets) - 1)) * packaging.h, packaging.pallet_shape[0] * packaging.h


def main():
    # Начальные данные
    pallet_width = 2000
    pallet_height = 2000
    drill_radius = 0
    eps = round(sqrt(1000 * 2000) / 50, 2) / 4

    packaging = Packing(pallet_height, pallet_width, eps, drill_radius)
    file_name = None
    file_name = 'src/input/NEST001-108.svg'
    # file_name = 'src/input/NEST002-216.svg'
    # file_name = 'src/input/NEST003-432.svg'

    # Инициализация предметов
    if file_name == None:
        polygons = create_list_of_items(100, pallet_height, pallet_width)
        # polygons2txt(polygons,
        #              path=r'src\output\polygons' + str(len(polygons)) + '.txt')
    else:
        polygons = svg_paths2polygons(file_name)
        # polygons2txt(polygons, path=r'src\output\NEST001-108.txt')
    # Жадный алгоритм
    print("\nШаг сетки:", eps)

    items, work_time, height, width = greedy_alg0(polygons, packaging)

    print("Использованная площадь:", height, "x", width)
    print("Время работы жадного алгоритма:", round(work_time, 2))
    print()

    # Отрисовка решения
    ann = "S = " + str(height) + " x " + str(width) + ";  time = " + str(
        round(work_time, 2)) + ";  Num_item = " + str(
            polygons.shape[0]) + ";  eps = " + str(eps)
    draw_all_pallets(items,
                     pallet_width,
                     pallet_height,
                     eps,
                     draw_pixels=False,
                     annotations=ann)
    return None


if __name__ == '__main__':
    main()
