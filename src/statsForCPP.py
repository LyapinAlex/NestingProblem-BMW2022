import time
import os.path
import numpy as np
from matplotlib import pyplot as plt

output_dir = 'src\\output'


def read_stats(path: str):
    f = open(path, 'r')
    stats = []
    line = f.readline()
    while line:
        list_values = line.split(' ')
        values = []
        for j in range(len(list_values) - 1):
            values.append(float(list_values[j]))
        line = f.readline()
        stats.append(values)
    f.close()
    return np.array(stats)


def draw_stats():
    save_file_name = "Результаты экспериментов" + ".png"
    annotations = "annotations"
    ylabel = "Длина используемой полосы"

    # Настройки вида графика
    fig, ax = plt.subplots()
    fig.set_figheight(7)
    fig.set_figwidth(10)
    # plt.title(annotations)
    plt.xlabel("Шаг сетки")
    plt.ylabel(ylabel)
    plt.grid(True)
    # ax.set_xscale('log', base=2)
    # ax.set_yscale('log', base=3)

    # Содержимое графика
    gridSteps = [i / 2 for i in range(50, 14, -1)]

    statsSE = read_stats(output_dir + "\\" + "Stats50SE.txt")
    mathE = np.mean(statsSE, axis=0, dtype=float)
    plt.plot(gridSteps, mathE, linestyle='-', label="Сегментный метод")

    statsASE = read_stats(output_dir + "\\" + "Stats50ASE.txt")
    mathE = np.mean(statsASE, axis=0, dtype=float)
    plt.plot(gridSteps, mathE, linestyle='-', color='r', label="Адаптивный сегментный метод")
    # plt.plot(gridSteps, mathE)

    ax.legend()
    plt.savefig(output_dir + "\\" + save_file_name)


def main():
    draw_stats()
    # stats = read_stats(output_dir + "\\" + "Stats50ASE.txt")
    # for line in stats:
    #     print(line)
    return


if __name__ == "__main__":
    main()