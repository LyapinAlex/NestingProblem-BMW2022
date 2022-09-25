from math import log, sqrt
import numpy as np
from matplotlib import pyplot as plt
import time

from data_rendering.draw_solution import draw_all_pallets
from putting_data.create_list_of_items import create_list_of_items
from putting_data.svg_paths2polygons import svg_paths2polygons
from class_item import Item
from class_pallet import Pallet
from new_greedy_alg.fit_pallets_with_rout import fit_pallets_with_rout


def new_greedy_alg0(polygons, pallet_width, pallet_height, eps, drill_radius):
    pal = Pallet(pallet_height, pallet_width, eps)

    # преобразование данных (создание растровых приближений)
    items = np.full(polygons.shape[0], None)
    for id in range(polygons.shape[0]):
        item = Item(id, polygons[id])
        item.creat_polygon_shell(drill_radius)
        item.list_of_new_shift_code(eps)
        items[id] = item

    # препроцессинги
    items = sorted(items, key=lambda item: -item.matrix.size)

    t_convert = time.time()
    # упаковка
    pallets = fit_pallets_with_rout(pal.shape, items, eps)

    # вычисление высоты первой паллеты
    i = 0
    while (i < pallets[len(pallets) - 1].shape[0]) and (
            pallets[len(pallets) - 1][i][0] != -pal.shape[0]):
        i += 1


    return time.time() - t_convert, (i + pal.shape[1] * (len(pallets) - 1)) * eps


def moment(mas, n=1):
    s = 0
    for it in mas:
        s += it**n
    return s / mas.size


def disp(mas):
    if mas.size == 1:
        return 0
    else:
        return sqrt(mas.size / (mas.size - 1) *
                    (moment(mas, 2) - moment(mas)**2))


def drow_stats(x, y, y_min, y_max, y_disp, xlabel="", ylabel="", annotations="No annotations", path = "src\output\stats.png"):
    fig, ax = plt.subplots()
    fig.set_figheight(7)
    fig.set_figwidth(10)
    plt.title(annotations)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    ax.set_yscale('log', base=1.86)
    ax.set_xscale('log', base=2)

    plt.plot(x, y, label = 'Среднее время решения')
    plt.plot(x, y,'b.')
    plt.plot(x, y + y_disp, 'k:', label = 'Стандартное откланение')
    plt.plot(x, y - y_disp, 'k:')
    plt.plot(x, y_max,'r.', label = 'Max/min время решения')
    plt.plot(x, y_min,'r.')

    ax.legend()
    plt.savefig(path)


def main1(num_it, num_eps=5):
    # Начальные данные
    pallet_width = 2000
    pallet_height = 1000
    drill_radius = 2

    work_time = np.zeros(num_eps)
    height = np.zeros(num_eps)

    eps = round(sqrt(pallet_height * pallet_width) / 50, 2)
    # ----------------------------------------------------------------------------------------
    for i in range(1, num_eps):
        eps0 = eps / i
        # Инициализация предметов
        polygons = create_list_of_items(num_it, pallet_height, pallet_width)
        # polygons = svg_paths2polygons('src/input/NEST001-108.svg')

        # Жадный алгоритм
        work_time[i], height[i] = new_greedy_alg0(polygons, pallet_width,
                                                  pallet_height, eps0,
                                                  drill_radius)

    return work_time[1:num_eps], height[1:num_eps]


def main2(num_exp = 10, num_item = 50, num_eps = 8):
    stats_t = np.zeros((num_exp, num_eps))
    stats_h = np.zeros((num_exp, num_eps))

    stats_t[0], stats_h[0] = main1(num_item, num_eps + 1)
    print(1, ':', num_exp)
    print("Прогнозируемое время работы: ", np.sum(stats_t[0]) * num_exp)
    for i in range(1, num_exp):
        stats_t[i], stats_h[i] = main1(num_item, num_eps + 1)
        print(i+1, ':', num_exp)

    eps = round(sqrt(1000 * 2000) / 50, 2)
    sr_time = 0
    eps_plt = np.zeros(num_eps)
    sr_time_plt = np.zeros(num_eps)
    sr_height_plt = np.zeros(num_eps)
    disp_time = np.zeros(num_eps)
    disp_height = np.zeros(num_eps)

    for i in range(num_eps):
        sr_time += moment(stats_t[:, i])
        eps_plt[i] = eps / (i + 1) 
        sr_time_plt[i] = round(moment(stats_t[:, i]), 4)
        sr_height_plt[i] = round(moment(stats_h[:, i]), 4)
        disp_time[i] = round(disp(stats_t[:, i]), 4)
        disp_height[i] = round(disp(stats_h[:, i]), 4)
    
    sr_time_plt_min = np.amin(stats_t, axis = 0)
    sr_time_plt_max = np.amax(stats_t, axis = 0)
    sr_height_plt_min = np.amin(stats_h, axis = 0)
    sr_height_plt_max = np.amax(stats_h, axis = 0)

    print("В среднем на один цикл:", sr_time)
    print("В сумме на все циклы:", sr_time * num_exp)
    print()


    drow_stats(eps_plt,
               sr_time_plt,
               sr_time_plt_min,
               sr_time_plt_max,
               disp_time,
               xlabel="Шаг сетки",
               ylabel="Среднее время работы",
               annotations="Запусков: " + str(num_exp) +
               "\nКоличество фигур: " + str(num_item),
               path = r"src\output\time_stats.png")
    
    drow_stats(eps_plt,
               sr_height_plt,
               sr_height_plt_min,
               sr_height_plt_max,
               disp_height,
               xlabel="Шаг сетки",
               ylabel="Средняя высота упаковки",
               annotations="Запусков: " + str(num_exp) +
               " Фигур в упаковке: " + str(num_item) +
               "\nРазмер паллеты: " + str(2000) + " x " + str(1000),
               path = r"src\output\height_stats.png")
    return stats_t, stats_h


if __name__ == '__main__':
    stats_t, stats_h = main2(num_exp = 10, num_item = 30, num_eps = 10)
    # f = open('output\stats.txt','w')
    # f.write("123")
    # print("\ntime:\n",stats_t)
    # print("\nheight:\n",stats_h)
    # f.close()

    
