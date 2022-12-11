import time
import os.path
import numpy as np
from matplotlib import pyplot as plt

from class_packing import Packing

results_dir = 'src\\output\\stats\\results'
experiments_dir = 'src\\output\\stats\\experiments'
charts_dir = 'src\\output\\stats\\charts'


def calc_num_files(path: str):
    num_files = len(
        [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    return num_files


def calc_stats_eps(packaging: Packing,
                   num_exp: int,
                   num_items: int,
                   eps: list,
                   save_file_name_h='',
                   save_file_name_t='',
                   initial_files=[],
                   is_save_polygons=False,
                   num_rot=4):
    """Если initial_files=[], сам генерирует тесты\\
        1"""
    stats_h = ''
    stats_t = ''

    if len(initial_files) != 0:
        packaging.input_dir = "src\\output\\stats\\experiments"
        num_exp = len(initial_files)
    # Упаковка примеров
    for i in range(num_exp):
        if len(initial_files) == 0:
            packaging.create_random_polygons(num_items)
        else:
            packaging.read_polygons_from_file(initial_files[i])

        if is_save_polygons:
            packaging.save_items_in_file(
                "stats\\experiments\\experiment" +
                str(calc_num_files(experiments_dir) - i) + " " + str(i) +
                ".txt")

        str_stat_h = ''
        str_stat_t = ''

        for h in eps:
            packaging.make_items(h, num_rout=num_rot)
            packaging.sort_items()
            packaging.greedy_packing()
            stat = packaging.get_stats()

            str_stat_h += str(stat[0]) + ' '
            str_stat_t += str(stat[1]) + ' '

        stats_h += str_stat_h + '\n'
        stats_t += str_stat_t + '\n'

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

    str_eps = ''
    for h in eps:
        str_eps += str(h) + ' '

    if save_file_name_h == '':
        save_path_h = results_dir + "\\stats_h" + str(
            calc_num_files(results_dir)) + ".txt"
    else:
        save_path_h = results_dir + "\\" + save_file_name_h
    if save_file_name_t == '':
        save_path_t = results_dir + "\\stats_t" + str(
            calc_num_files(results_dir)) + ".txt"
    else:
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

    print("Текущее время", time.strftime("%H:%M:%S", time.localtime()))
    print("\nРабота завершена, результаты сохранены в \n" + save_path_h +
          "\n" + save_path_t + "\n")

    return None


def pick_one(packaging: Packing, eps: float, file_name: str):
    packaging.input_dir = "src\\output\\stats\\experiments"
    packaging.read_polygons_from_file(file_name)
    packaging.make_items(eps, 4)
    packaging.sort_items()
    packaging.greedy_packing()

    # Результаты упаковки
    packaging.change_position()
    packaging.clear_output()
    packaging.save_pallets_in_files('pallet.png')
    return


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


def draw_stats_different_eps(file_name: str, is_time_stats=True):
    path = results_dir + "\\" + file_name
    num_exp, num_items, stats_eps, stats_of_exp = read_stats(path)

    if is_time_stats:
        expected_label = "Среднее время решения"
        min_max_label = "Max/min время решения"
        save_path = charts_dir + "\\time_stats " + str(
            calc_num_files(charts_dir)) + ".png"
    else:
        expected_label = "Средняя высота решения"
        min_max_label = "Max/min высота решения"
        save_path = charts_dir + "\\height_stats " + str(
            calc_num_files(charts_dir)) + ".png"

    # Настройки вида графика
    fig, ax = plt.subplots()
    fig.set_figheight(7)
    fig.set_figwidth(10)
    annotations = "Запусков: " + str(num_exp) + "\nФигур в упаковке: " + str(
        num_items)
    plt.title(annotations)
    plt.xlabel("Шаг сетки")
    plt.ylabel("Время работы алгоритма")
    plt.grid(True)

    # Содержимое графика
    expected_value = np.mean(stats_of_exp, axis=0, dtype=float)
    standard_deviation = np.std(stats_of_exp, axis=0, dtype=float)
    maximum_value = np.amax(stats_of_exp, axis=0)
    minimum_value = np.amin(stats_of_exp, axis=0)

    plt.plot(stats_eps, expected_value, label=expected_label)
    plt.plot(stats_eps, expected_value, 'b.')

    plt.plot(stats_eps,
             expected_value + standard_deviation,
             'k:',
             label="Стандартное отклонение")
    plt.plot(stats_eps, expected_value - standard_deviation, 'k:')

    plt.plot(stats_eps, maximum_value, 'r.', label=min_max_label)
    plt.plot(stats_eps, minimum_value, 'r.')

    ax.legend()
    plt.savefig(save_path)
    return


def draw_stats_different_packing(file_names: list,
                                 lables_of_path=[],
                                 save_file_name='',
                                 ylabel="Среднее время работы алгоритма",
                                 annotations="Сравнение разных упаковок"):

    if len(lables_of_path) != 0 and len(lables_of_path) != len(file_names):
        raise Exception("Названий линий больше/меньше, чем фалов")

    if save_file_name == '':
        save_path = charts_dir + "\\different_packing" + str(
            calc_num_files(charts_dir)) + ".png"
    else:
        save_path = charts_dir + "\\" + save_file_name

    # Настройки вида графика
    fig, ax = plt.subplots()
    fig.set_figheight(7)
    fig.set_figwidth(10)
    plt.title(annotations)
    plt.xlabel("Шаг сетки")
    plt.ylabel(ylabel)
    plt.grid(True)
    ax.set_xscale('log', base=2)
    # ax.set_yscale('log', base=3)

    # Содержимое графика
    for num_path in range(len(file_names)):
        num_exp, num_items, stats_eps, stats_of_exp = read_stats(
            results_dir + "\\" + file_names[num_path])

        expected_value = np.mean(stats_of_exp, axis=0, dtype=float)
        if len(lables_of_path) != 0:
            expected_label = lables_of_path[num_path]
        else:
            expected_label = 'num_exp=' + str(num_exp) + '  num_items=' + str(
                num_items)

        plt.plot(stats_eps, expected_value, label=expected_label)
        plt.plot(stats_eps, expected_value, 'b.')

    ax.legend()
    plt.savefig(save_path)

    return


def bar_diag(file_names, lables_of_path, xlabel = "Шаг сетки", ylabel = "Высота", title = "Среднее отклонение"):
    f = open(results_dir + "\\" + file_names[0], 'r')
    f.readline()
    f.readline()
    list_eps = f.readline().split(' ')
    f.close()

    num_column = len(file_names)
    num_groups = len(list_eps) - 1

    ind = np.arange(num_groups)
    width = 1 / (num_column + 2)
    bars = []
    stats_eps = None
    for i in range(num_column):
        num_exp, num_items, stats_eps, stats_of_exp = read_stats(results_dir +
                                                                 "\\" +
                                                                 file_names[i])
        expected_value = np.mean(stats_of_exp, axis=0, dtype=float)
        standard_deviation = np.std(stats_of_exp, axis=0, dtype=float)
        bar = plt.bar(ind + width * i, standard_deviation, width)
        bars.append(bar)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.xticks(ind + width/2 * (num_column-1), stats_eps)
    plt.legend(bars, lables_of_path)
    plt.show()
    return


def main0():
    """проверить одно решение"""
    pack = Packing(width=2000, height=1000, drill_radius=0)
    pick_one(pack, 4, "experiment1 0.txt")
    return


def main1():
    """сбор статистики"""
    pack = Packing(width=2000, height=1000, drill_radius=0)
    calc_stats_eps(packaging=pack,
                   num_exp=100,
                   num_items=100,
                   eps=[4.375, 6.25, 8.75, 12.5, 17.5, 25, 35, 50, 70, 100],
                   save_file_name_h='rot0_100_h' +
                   str(calc_num_files(results_dir)) + '.txt',
                   save_file_name_t='rot0_100_t' +
                   str(calc_num_files(results_dir)) + '.txt',
                   is_save_polygons=True)
    return


def main2():
    """сбор статистики из существующих тестов"""
    for num_rotation in range(3, 5):
        pack = Packing(width=2000, height=1000, drill_radius=0)
        init_files = ['experiment1 ' + str(i) + '.txt' for i in range(100)]
        calc_stats_eps(
            packaging=pack,
            num_exp=0,
            num_items=100,
            eps=[4.375, 6.25, 8.75, 12.5, 17.5, 25, 35, 50, 70, 100],
            save_file_name_h='rot' + str(num_rotation) + '_100_h' +
            str(calc_num_files(results_dir)) + '.txt',
            save_file_name_t='rot' + str(num_rotation) + '_100_t' +
            str(calc_num_files(results_dir)) + '.txt',
            initial_files=init_files,
            num_rot=num_rotation)
    return


def main4():
    """отрисовка одного файла"""
    draw_stats_different_eps(r'rot4_t0.txt')
    draw_stats_different_eps(r'rot4_h0.txt', is_time_stats=False)
    return


def main5():
    """отрисовка нескольких файлов в одном графике"""
    file_names = [
        # 'rot0_t4.txt', 'rot1_t6.txt', 'rot2_t8.txt',
        # 'rot3_t10.txt', 'rot4_t2.txt',
        'rot0_100_t12.txt',
        'rot1_100_t14.txt',
        'rot2_100_t16.txt',
        'rot3_100_t18.txt',
        'rot4_100_t20.txt'
    ]
    lables_of_path = [
        # "Без поворота (70)",
        # "На длиннейшую сторону (70)",
        # "На случайную сторону (70)",
        # "Поворот* (70)",
        # "Минимальная площадь описанного прямоугольника (70)",
        "Без поворота (100)",
        "На длиннейшую сторону (100)",
        "На случайную сторону (100)",
        "Поворот* (100)",
        "Минимальная площадь описанного прямоугольника (100)",
    ]
    draw_stats_different_packing(
        file_names,
        lables_of_path,
        # save_file_name = '100it_100exp_t',
        # ylabel = "Средняя высота упаковки",
        annotations='Сравнение разных упаковок при объёме выборки n = 100')
    return


def main6():
    """Представление данных в виде диаграммы"""
    file_names = [
        # 'rot0_h4.txt', 'rot1_h6.txt', 'rot2_h8.txt',
        # 'rot3_h10.txt', 'rot4_h2.txt',
        'rot0_100_h12.txt',
        'rot1_100_h14.txt',
        'rot2_100_h16.txt',
        'rot3_100_h18.txt',
        'rot4_100_h20.txt'
    ]
    lables_of_path = [
        # "Without rotation (70)",
        # "The longest side (70)",
        # "Random side (70)",
        # "Rotation* (70)",
        # "Min area (70)",
        "Without rotation (100)",
        "The longest side (100)",
        "Random side (100)",
        "Rotation* (100)",
        "Min area (100)"
    ]
    bar_diag(file_names, lables_of_path)
    return


if __name__ == '__main__':
    main6()