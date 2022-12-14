import math
import random
import time
import numpy as np
from matplotlib import pyplot as plt
from class_nfp_packer import Nfp_Packer
from class_packing import Packing
from class_item import Item
from class_polygon import Polygon
from data_rendering.items2png import items2png

# Датасеты: https://www.euro-online.org/websites/esicup/data-sets/

# ------------- Функции чтения файлов определённых типов -------------


def packing_from_our_tests(input_file_name: str,
                           input_dir="src\\input\\concave50\\",
                           is_draw=True,
                           is_print_stats=True,
                           num_rot=4,
                           num_sort=2,
                           eps=0.0):
    """Входные данные типа test1"""
    # ------------  чтение файла  ------------
    path = input_dir + input_file_name
    f = open(path, 'r')
    num_items = int(f.readline())
    polygons = []
    list_pallet_shape = f.readline().split(' ')
    for i in range(num_items):
        list_points = f.readline().split(' ')
        points = []
        for j in range(0, len(list_points) - 1, 2):
            point = [float(list_points[j]), float(list_points[j + 1])]
            points.append(point)
        if (points[0][0] == points[-1][0] and points[0][1] == points[-1][1]):
            points.pop()
        poly = Polygon(points)
        poly.sort_points()
        poly.expanded_polygon = poly.expand_polygon(0.01)
        polygons.append(poly)

    f.close()
    # ------------  Задание данных  ------------
    pallet = Nfp_Packer(
        float(list_pallet_shape[1]), float(list_pallet_shape[0]))

    i = 0
    items = []
    packaging = Packing(width=float(list_pallet_shape[1]),
                        height=float(list_pallet_shape[0]),
                        drill_radius=0)
    # polygons.sort(lambda x: - x.area)
    start_time = time.time()
    polygons = sorted(polygons, key=lambda x: -x.area)
    for polygon in polygons:
        i += 1
        print(i)
        try:
            pallet.pack(polygon, with_rotation=True)
        except:
            return None
        items.append(Item(i, polygon.points_to_list()))
    print('Затраченое время:', time.time() - start_time)
    packaging.time_packing = time.time()-start_time
    packaging.num_packing_items = num_items
    packaging.target_height = round(pallet.max_y, 2)
    packaging.target_width = round(pallet.max_x, 2)

    if is_print_stats:
        packaging.print_stats()
    if is_draw:
        # packaging.change_position()
        # packaging.save_pallets_in_files(input_file_name[0:-3] + 'png')
        items2png(r'C:\Users\1\Desktop\NestingProblem-BMW2022\src\output\\' + input_file_name[0:-3] + 'png',
                  items, packaging, False)
    return packaging.get_stats()


def packing_from_Terashima2(input_file_name: str,
                            is_draw=False,
                            is_print_stats=True,
                            num_rot=4,
                            num_sort=2,
                            eps=0.0):
    """Входные данные типа Terashima2 (распаковываем интересующие файлы и запускаем)"""
    # ------------  чтение файла  ------------
    path = "src\\input\\dataset" + input_file_name
    f = open(path, 'r')
    num_items = int(f.readline())
    polygons = np.full(num_items, None)
    list_pallet_shape = f.readline().split(' ')
    for i in range(num_items):
        list_points = f.readline().split(' ')
        points = []
        for j in range(2, len(list_points) - 1, 2):
            point = [float(list_points[j]), float(list_points[j + 1])]
            points.append(point)
        if (points[0][0] == points[-1][0] and points[0][1] == points[-1][1]):
            points.pop()
        polygons[i] = np.array(points)
    f.close()
    # ------------  Задание данных  ------------
    pallet = Nfp_Packer(
        float(list_pallet_shape[1]), float(list_pallet_shape[0]))

    i = 0
    items = []
    packaging = Packing(width=float(list_pallet_shape[1]),
                        height=float(list_pallet_shape[0]),
                        drill_radius=0)
    # polygons.sort(lambda x: - x.area)
    start_time = time.time()
    polygons = sorted(polygons, key=lambda x: -x.area)
    for polygon in polygons:
        i += 1
        pallet.pack(polygon, with_rotation=False)
        items.append(Item(i, polygon.points_to_list()))
    print('Затраченое время:', time.time() - start_time)
    packaging.time_packing = time.time()-start_time
    packaging.num_packing_items = num_items
    packaging.target_height = round(pallet.max_y, 2)
    packaging.target_width = round(pallet.max_x, 2)

    if is_print_stats:
        packaging.print_stats()
    if is_draw:
        # packaging.change_position()
        # packaging.save_pallets_in_files(input_file_name[0:-3] + 'png')
        items2png(r'C:\Users\1\Desktop\NestingProblem-BMW2022\src\output\\' +
                  input_file_name[0:-3] + 'png', items, packaging, False)
    return packaging.get_stats()


def packing_from_swim(input_file_name: str,
                      is_draw=True,
                      is_print_stats=True,
                      width=10000,
                      height=5752,
                      num_rot=4,
                      num_sort=2,
                      eps=0.0):
    """Входные данные типа swim.txt (trousers.txt, shirts.txt, ...)"""
    # ------------  чтение файла  ------------
    path = "src\\input\\dataset\\" + input_file_name
    f = open(path, 'r')
    line = f.readline()
    polygons = []
    while line:
        f.readline()  # QUANTITY
        quantity = int(f.readline().split(' ')[0][:-1])
        f.readline()  # NUMBER OF VERTICES
        num_verties = int(f.readline().split(' ')[0][:-1])
        f.readline()  # VERTICES (X,Y)
        polygon = []
        for _ in range(num_verties):
            line = f.readline()
            list_point = (''.join([
                line[i] for i in range(len(line) - 1)
                if not ((line[i] == ' ') and (line[i + 1] == ' '))
            ])).split(' ')
            point = [float(list_point[-2]), float(list_point[-1])]
            polygon.append(point)
        for _ in range(quantity):
            poly = Polygon(polygon)
            poly.rotate(math.pi/2)
            poly.rotate(random.random()/30)
            poly.sort_points()
            poly.expanded_polygon = poly.expand_polygon(0.01)
            polygons.append(poly)
        f.readline()  #
        line = f.readline()  # PIECE k
    f.close()
    # ------------  Задание данных  ------------
    pallet = Nfp_Packer(
        float(height), float(width))

    i = 0
    items = []
    packaging = Packing(width=float(height),
                        height=float(width),
                        drill_radius=0)
    # polygons.sort(lambda x: - x.area)
    start_time = time.time()
    polygons = sorted(polygons, key=lambda x: -x.area)
    i = 0
    for polygon in polygons:
        i += 1
        print(i)
        pallet.pack(polygon, with_rotation=True)
        items.append(Item(i, polygon.points_to_list()))
    print('Затраченое время:', time.time() - start_time)
    packaging.time_packing = time.time()-start_time
    packaging.num_packing_items = len(pallet.polygons)
    packaging.target_height = round(pallet.max_y, 2)
    packaging.target_width = round(pallet.max_x, 2)
    if is_print_stats:
        packaging.print_stats()
    if is_draw:
        # packaging.change_position()
        # packaging.save_pallets_in_files(input_file_name[0:-3] + 'png')
        items2png(r'C:\Users\1\Desktop\NestingProblem-BMW2022\src\output\\' +
                  input_file_name[0:-3] + 'png', items, packaging, False)
    return packaging.get_stats()


# ---------------------------- Статистика ----------------------------

results_dir = 'src\\output\\stats\\results'
charts_dir = 'src\\output\\stats\\charts'


def create_pack(output_file_name: str,
                num_items: int,
                width=2000,
                height=1000):
    packaging = Packing(width=width,
                        height=height,
                        drill_radius=0,
                        border_distance=0)
    packaging.create_random_polygons(num_items)
    packaging.output_dir = "src\\input\\concave30"
    packaging.save_items_in_file(output_file_name, False)
    return


def collect_stats(initial_files: list[str],
                  list_eps: list,
                  input_dir: str,
                  save_file_name_h: str,
                  save_file_name_t: str,
                  num_rot=4,
                  num_sort=2):
    stats_h = ''
    stats_t = ''
    num_exp = len(initial_files)

    f = open(input_dir + initial_files[0], 'r')
    num_items = int(f.readline())
    f.close()
    # Сбор статистики
    for i in range(num_exp):
        str_stat_h = ''
        str_stat_t = ''

        for h in list_eps:
            stat = packing_from_our_tests(initial_files[i],
                                          input_dir,
                                          num_rot=num_rot,
                                          num_sort=num_sort,
                                          eps=h,
                                          is_print_stats=False)
            if (stat is None):
                continue
            str_stat_h += str(stat[0]) + ' '
            str_stat_t += str(stat[1]) + ' '

        stats_h += str_stat_h + '\n'
        stats_t += str_stat_t + '\n'
        # Отслеживание работы
        if i == 0:
            list_timings = str_stat_t.split(' ')
            time_one_iter = 0
            for timing in list_timings:
                if timing != '':
                    time_one_iter += float(timing)
            print("\nВремя одной итерации: ", round(time_one_iter, 3))
            print("Текущее время", time.strftime("%H:%M:%S", time.localtime()))
            print("Прогнозируемое время работы: ",
                  int(time_one_iter * num_exp // 60), ":",
                  round(time_one_iter * num_exp % 60), "\n")

        print(i + 1, '/', num_exp)
    # Сохранение статистики
    str_eps = ''
    for h in list_eps:
        str_eps += str(h) + ' '

    save_path_h = results_dir + "\\" + save_file_name_h
    save_path_t = results_dir + "\\" + save_file_name_t

    initial_data = str(num_exp) + '\n' + str(num_items) + '\n' + str_eps + '\n'

    f = open(save_path_h, 'w')
    f.write(initial_data)
    f.write(stats_h)
    f.close()

    f = open(save_path_t, 'w')
    f.write(initial_data)
    f.write(stats_t)
    f.close()

    print("\nТекущее время", time.strftime("%H:%M:%S", time.localtime()))
    print("\nРабота завершена, результаты сохранены в \n" + save_path_h +
          "\n" + save_path_t + "\n")

    return None


def collect_stats_from_swim(initial_files: list[str],
                            list_eps: list,
                            save_file_name_h: str,
                            save_file_name_t: str,
                            width=10000,
                            height=5752,
                            num_rot=4,
                            num_sort=2):
    stats_h = ''
    stats_t = ''
    num_exp = len(initial_files)
    num_items = -1  # пока пофиг

    # Сбор статистики
    for i in range(num_exp):
        str_stat_h = ''
        str_stat_t = ''

        for h in list_eps:
            stat = packing_from_swim(initial_files[i],
                                     is_print_stats=False,
                                     width=width,
                                     height=height,
                                     num_rot=num_rot,
                                     num_sort=num_sort,
                                     eps=h)
            str_stat_h += str(stat[0]) + ' '
            str_stat_t += str(stat[1]) + ' '

        stats_h += str_stat_h + '\n'
        stats_t += str_stat_t + '\n'
        # Отслеживание работы
        if i == 0:
            list_timings = str_stat_t.split(' ')
            time_one_iter = 0
            for timing in list_timings:
                if timing != '':
                    time_one_iter += float(timing)
            print("\nВремя одной итерации: ", round(time_one_iter, 3))
            print("Текущее время", time.strftime("%H:%M:%S", time.localtime()))
            print("Прогнозируемое время работы: ",
                  int(time_one_iter * num_exp // 60), ":",
                  round(time_one_iter * num_exp % 60), "\n")

        print(i + 1, '/', num_exp)
    # Сохранение статистики
    str_eps = ''
    for h in list_eps:
        str_eps += str(h) + ' '

    save_path_h = results_dir + "\\" + save_file_name_h
    save_path_t = results_dir + "\\" + save_file_name_t

    initial_data = str(num_exp) + '\n' + str(num_items) + '\n' + str_eps + '\n'

    f = open(save_path_h, 'w')
    f.write(initial_data)
    f.write(stats_h)
    f.close()

    f = open(save_path_t, 'w')
    f.write(initial_data)
    f.write(stats_t)
    f.close()

    print("\nТекущее время", time.strftime("%H:%M:%S", time.localtime()))
    print("\nРабота завершена, результаты сохранены в \n" + save_path_h +
          "\n" + save_path_t + "\n")

    return None


# ------------------- Отрисовка/подсчёт статистики -------------------


def read_stats(path: str):
    f = open(path, 'r')
    num_exp = int(f.readline())
    num_items = int(f.readline())

    list_eps = f.readline().split(' ')
    epsilons = []
    for j in range(len(list_eps) - 1):  # -1 т.к. строка заканчивается '\n'
        epsilons.append(float(list_eps[j]))
    stats_eps = np.array(epsilons)

    stats_of_exp = np.full((num_exp, len(list_eps) - 1), None)
    for i in range(num_exp):
        list_values = f.readline().split(' ')
        values = []
        for j in range(len(list_values) -
                       1):  # -1 т.к. строка заканчивается '\n'
            values.append(float(list_values[j]))
        stats_of_exp[i] = np.array(values)
    f.close()
    return num_exp, num_items, stats_eps, stats_of_exp


def culc_stats(file_name):
    num_exp, num_items, stats_eps, stats_of_exp = read_stats(results_dir +
                                                             "\\" + file_name)
    expected_value = np.mean(stats_of_exp, axis=0, dtype=float)
    standard_deviation = np.std(stats_of_exp, axis=0, dtype=float)
    maximum_value = np.amax(stats_of_exp, axis=0)
    minimum_value = np.amin(stats_of_exp, axis=0)
    print("file_name:", file_name)
    print("Шаги сетки:", stats_eps)
    print("Среднее:", expected_value)
    print("Стандартное откланение:", standard_deviation)
    print("Максимальное зачение:", maximum_value)
    print("Минимальное зачение:", minimum_value)
    print()
    return expected_value, standard_deviation, maximum_value, minimum_value


def draw_stats(file_names: list[str], lables_of_path: list[str],
               save_file_name: str, ylabel: str, annotations: str):

    if len(lables_of_path) != 0 and len(lables_of_path) != len(file_names):
        raise Exception("Названий линий больше/меньше, чем фалов")

    # Настройки вида графика
    fig, ax = plt.subplots()
    fig.set_figheight(7)
    fig.set_figwidth(10)
    plt.title(annotations)
    plt.xlabel("Шаг сетки")
    plt.ylabel(ylabel)
    plt.grid(True)
    # ax.set_xscale('log', base=2)

    # Содержимое графика
    for num_path in range(len(file_names)):
        num_exp, num_items, stats_eps, stats_of_exp = read_stats(
            results_dir + "\\" + file_names[num_path])

        expected_value = np.mean(stats_of_exp, axis=0, dtype=float)
        if len(lables_of_path) != 0:
            plt.plot(stats_eps, expected_value, label=lables_of_path[num_path])
        else:
            plt.plot(stats_eps, expected_value)
        plt.plot(stats_eps, expected_value, 'b.')
    if len(lables_of_path) != 0:
        ax.legend()
    save_path = charts_dir + "\\" + save_file_name
    plt.savefig(save_path)


def main1():
    """Сбор статистики из наших тестов"""
    input_dir = "src\\input\\concave30\\"
    init_files = ['test' + str(i) + '.txt' for i in range(34, 35)]
    list_eps = [0.01]
    save_file_name_time = "NFP-time.txt"
    save_file_name_height = "NFP-height.txt"
    collect_stats(init_files, list_eps, input_dir, save_file_name_height,
                  save_file_name_time)
    return


def main2():
    """Сбор статистики из тестов типа swim с датасета"""
    init_files = ["shirts.txt"]
    width = 100
    height = 40

    # init_files = ["trousers.txt"]
    # width = 500
    # height = 79

    # init_files = ["swim.txt"]
    # width = 10000
    # height = 5752

    list_eps = [0.01]
    save_file_name_time = "NFP-SWIM-time1.txt"
    save_file_name_height = "NFP-SWIM-height1.txt"
    collect_stats_from_swim(init_files, list_eps, save_file_name_height,
                            save_file_name_time, width, height)
    return


def main3():
    """Отрисовка статистики (можно из нескольки файлов)"""
    file_names = ["my_tests-height.txt"]
    lables_of_path = []
    save_file_name = "my_tests-height"
    ylabel = ""
    annotations = ""
    draw_stats(file_names, lables_of_path, save_file_name, ylabel, annotations)
    return


if __name__ == '__main__':
    # for i in range(0,1):
    #     ### create_pack('test'+str(i)+'.txt', 30, 210, 100)
    #     [height, time] = packing_from_our_tests(input_file_name='test'+str(i)+'.txt', input_dir = "src\\input\\concave30\\")

    # [height, time] = packing_from_swim('shirts.txt',
    #                                    True,
    #                                    width=100,
    #                                    height=40)

    # [height, time] = packing_from_swim('trousers.txt',
    #                                    True,
    #                                    width=500,
    #                                    height=79)

    # [height, time] = packing_from_swim('swim.txt',
    #                                    True,
    #                                    width=10000,
    #                                    height=5752)

    # culc_stats("NFP-time.txt")
    # culc_stats("NFP-height.txt")
    main1()
    # main2()
