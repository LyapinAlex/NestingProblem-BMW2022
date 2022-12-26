import time
import numpy as np
from matplotlib import pyplot as plt
from class_packing import Packing
from class_item import Item

# Датасеты: https://www.euro-online.org/websites/esicup/data-sets/

# ------------- Функции чтения файлов определённых типов -------------


def packing_from_our_tests(input_file_name: str,
                           input_dir="src\\input\\concave50\\",
                           is_draw=False,
                           is_print_stats=True,
                           num_rot=0,
                           num_sort=2,
                           eps=0.0):
    """Входные данные типа test1"""
    # ------------  чтение файла  ------------
    path = input_dir + input_file_name
    f = open(path, 'r')
    num_items = int(f.readline())
    polygons = np.full(num_items, None)
    list_pallet_shape = f.readline().split(' ')
    for i in range(num_items):
        list_points = f.readline().split(' ')
        points = []
        for j in range(0, len(list_points) - 1, 2):
            point = [float(list_points[j]), float(list_points[j + 1])]
            points.append(point)
        if (points[0][0] == points[-1][0] and points[0][1] == points[-1][1]):
            points.pop()
        polygons[i] = np.array(points)
    f.close()
    # ------------  Задание данных  ------------
    packaging = Packing(width=float(list_pallet_shape[0]),
                        height=float(list_pallet_shape[1]),
                        drill_radius=0,
                        border_distance=0)
    packaging.polygons = polygons
    packaging.num_items = num_items
    packaging.items = np.full(packaging.num_items, None)
    for id in range(packaging.num_items):
        item = Item(id, polygons[id])
        packaging.items[id] = item
    # ------------  Упаковка  ------------
    packaging.make_items(h=eps, num_rout=num_rot)
    packaging.sort_items(num_sort=num_sort)
    packaging.greedy_packing()

    if is_print_stats:
        packaging.print_stats()
    if is_draw:
        packaging.change_position()
        packaging.save_pallets_in_files(input_file_name[0:-3] + 'png')
    return packaging.get_stats()


def packing_from_Terashima2(input_file_name: str,
                            is_draw=False,
                            is_print_stats=True,
                            num_rot=0,
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
    packaging = Packing(width=float(list_pallet_shape[1]),
                        height=float(list_pallet_shape[2]),
                        drill_radius=0,
                        border_distance=0)
    packaging.polygons = polygons
    packaging.num_items = num_items
    packaging.items = np.full(packaging.num_items, None)
    for id in range(packaging.num_items):
        item = Item(id, polygons[id])
        packaging.items[id] = item
    # ------------  Упаковка  ------------
    packaging.make_items(h=eps, num_rout=num_rot)
    packaging.sort_items(num_sort=num_sort)
    packaging.greedy_packing()

    if is_print_stats:
        packaging.print_stats()
    if is_draw:
        packaging.change_position()
        packaging.save_pallets_in_files(input_file_name[0:-3] + 'png')
    return packaging.get_stats()


def packing_from_swim(input_file_name: str,
                      is_draw=False,
                      is_print_stats=True,
                      width=10000,
                      height=5752,
                      num_rot=0,
                      num_sort=2,
                      eps=0.0):
    """Входные данные типа swim.txt (trousers.txt, shirts.txt, ...)"""
    # ------------  чтение файла  ------------
    path = "src\\input\\dataset\\" + input_file_name
    f = open(path, 'r')
    line = f.readline()
    polygons = []
    while line:
        f.readline()  #QUANTITY
        quantity = int(f.readline().split(' ')[0][:-1])
        f.readline()  #NUMBER OF VERTICES
        num_verties = int(f.readline().split(' ')[0][:-1])
        f.readline()  #VERTICES (X,Y)
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
            polygons.append(polygon)
        f.readline()  #
        line = f.readline()  #PIECE k
    f.close()
    # ------------  Задание данных  ------------
    packaging = Packing(width=width,
                        height=height,
                        drill_radius=0,
                        border_distance=0)

    packaging.polygons = np.array(polygons, dtype=object)
    packaging.num_items = len(polygons)
    packaging.items = np.full(packaging.num_items, None)
    for id in range(packaging.num_items):
        item = Item(id, polygons[id])
        packaging.items[id] = item
    # ------------  Упаковка  ------------
    packaging.make_items(h=eps, num_rout=num_rot)
    packaging.sort_items(num_sort=num_sort)
    packaging.greedy_packing()

    if is_print_stats:
        packaging.print_stats()
    if is_draw:
        packaging.change_position()
        packaging.save_pallets_in_files(input_file_name[0:-3] + 'png')
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
                  num_rot=0,
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
                                          is_draw=False,
                                          is_print_stats=False)
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
                  num_rot=0,
                  num_sort=2):
    stats_h = ''
    stats_t = ''
    num_exp = len(initial_files)
    num_items = -1 # пока пофиг

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


def main1(dirict = "concave15"):
    """Сбор статистики из наших тестов"""
    input_dir = "src\\input\\"+dirict+"\\"
    init_files = ['test' + str(i) + '.txt' for i in range(50)]
    list_eps = [0.5, 1, 2]
    save_file_name_time = dirict+"-time.txt"
    save_file_name_height = dirict+"-height.txt"
    collect_stats(init_files, list_eps, input_dir, save_file_name_height,
                  save_file_name_time)
    return


def main2(file_name = "shirts"):
    """Сбор статистики из тестов типа swim с датасета"""
    if file_name == "swim":
        init_files = ["swim.txt"]
        width=10000
        height=5752
        list_eps = [36, 18]
    elif file_name == "trousers":
        init_files = ["trousers.txt"]
        width=500
        height=79
        list_eps = [1, 0.5]
    elif file_name == "shirts":
        init_files = ["shirts.txt"]
        width=100
        height=40
        list_eps = [1, 0.5]

    save_file_name_time = file_name+"-time.txt"
    save_file_name_height = file_name+"-height.txt"
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
    # main1("convex15")
    # main1("convex30")
    # main1("concave15")
    # main1("concave30")
    
    # culc_stats("convex15-height.txt")
    # culc_stats("convex30-height.txt")
    # culc_stats("concave15-height.txt")
    # culc_stats("concave30-height.txt")

    # culc_stats("convex15-time.txt")
    # culc_stats("convex30-time.txt")
    # culc_stats("concave15-time.txt")
    # culc_stats("concave30-time.txt")

    packing_from_our_tests("test22.txt", "src\\input\\concave15\\", True, eps = 0.5)
    # packing_from_our_tests("test43.txt", "src\\input\\convex15\\", True, eps = 1)
    # packing_from_swim("swim.txt", True)
    # main2("swim")
    # main2("trousers")
    # main2("shirts")

    # packing_from_swim("swim.txt", True, True, 10000, 5752, eps=18)
    # packing_from_swim("trousers.txt", True, True, 500, 79, eps=0.5)
    # packing_from_swim("shirts.txt", True, True, 100, 40, eps=0.5)