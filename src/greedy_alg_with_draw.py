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


def greedy_alg_with_draw(polygons, packaging):
    t_convert = time.time()
    # преобразование данных (создание растровых приближений)
    items = np.full(polygons.shape[0], None)
    for id in range(polygons.shape[0]):
        item = Item(id, polygons[id])
        item.creat_polygon_shell(packaging.drill_radius)
        item.list_of_new_shift_code(packaging.h)
        items[id] = item

    t_packing = time.time()
    # препроцессинги
    items = sorted(items, key=lambda item: -item.matrix.size)
    # items2txt(items, path=r'src\output\items'+str(len(polygons))+'.txt')
    # упаковка
    pallets = fit_pallets_with_rotation(packaging.pallet_shape, items,
                                        packaging.h)

    t_finish = time.time()
    # вычисление целевой высоты
    i = 0
    while (i < pallets[len(pallets) - 1].shape[0]) and (
            pallets[len(pallets) - 1][i][0] != -packaging.pallet_shape[0]):
        i += 1
    #сохранение статистики
    packaging.num_packing_items = polygons.shape[0]  #пока что формально стоит
    packaging.target_width = packaging.pallet_shape[0] * packaging.h
    packaging.target_height = (i + packaging.pallet_shape[1] *
                               (len(pallets) - 1)) * packaging.h
    packaging.time_convert_data = round(t_packing - t_convert, 2)
    packaging.time_packing = round(t_finish - t_packing, 2)

    return items


def main():
    # Начальные данные
    pallet_width = 2000
    pallet_height = 1000
    drill_radius = 0
    eps = round(sqrt(1000 * 2000) / 50, 2) / 2

    packaging = Packing(pallet_width, pallet_height, eps, drill_radius)
    file_name = None
    # file_name = 'src/input/NEST001-108.svg'
    # file_name = 'src/input/NEST002-216.svg'
    # file_name = 'src/input/NEST003-432.svg'

    # Инициализация предметов
    if file_name == None:
        polygons = create_list_of_items(200, pallet_height, pallet_width)
    else:
        polygons = svg_paths2polygons(file_name)
    # polygons2txt(polygons, path=r'src\output\polygons' + str(len(polygons)) + '.txt')
    # Жадный алгоритм
    items = greedy_alg_with_draw(polygons, packaging)

    # Результаты упаковки
    packaging.print_stats()
    draw_all_pallets(items, packaging, draw_pixels=False)
    return None


if __name__ == '__main__':
    main()
