import time
import numpy as np
from matplotlib import pyplot as plt

# from .class_packing import Packing
# from .data_writer.primitives import calc_num_files

from class_packing import Packing
from data_writer.primitives import calc_num_files, settings_function_graph


class Stats:

    def __init__(
            self,
            experiments_dir='Compressed_encoding\\input\\stats_experiments-1',
            results_dir='Compressed_encoding\\output\\stats_results',
            charts_dir='Compressed_encoding\\output\\stats_charts'):

        # -------  Directories  ------
        self.__experiments_dir = experiments_dir
        self.__results_dir = results_dir
        self.__charts_dir = charts_dir

        # ----  Stats parameters  ----
        self.__list_eps: list[float] = []

    def append_grid_step(self, eps) -> None:
        self.__list_eps.append(eps)

    def remove_grid_steps(self) -> None:
        self.__list_eps: list[float] = []

    def create_tests(self, num_tests: int, num_items: int,
                     pallet_height: float, pallet_width: float) -> None:
        for num_test in range(num_tests):
            pack = Packing("src\\input", self.__experiments_dir)
            pack.set_packaging_parameters(pallet_height, pallet_width)
            pack.create_random_polygons(num_items)
            pack.save_raw_data("test" + str(num_test) + ".txt")

    def __save_stats(self,
                     num_files: int,
                     stats_h: str,
                     stats_t: str,
                     save_file_name_h='',
                     save_file_name_t='') -> None:
        str_eps = ''
        for eps in self.__list_eps:
            str_eps += str(eps) + ' '

        if save_file_name_h == '':
            save_path_h = self.__results_dir + "\\stats_h-"
            save_path_h += str(
                calc_num_files(self.__results_dir) // 2) + ".txt"
        else:
            save_path_h = self.__results_dir + "\\" + save_file_name_h

        if save_file_name_t == '':
            save_path_t = self.__results_dir + "\\stats_t-"
            save_path_t += str(
                calc_num_files(self.__results_dir) // 2) + ".txt"
        else:
            save_path_t = self.__results_dir + "\\" + save_file_name_t

        initial_data = str(num_files) + '\n' + str_eps + '\n'

        f = open(save_path_h, 'w')
        f.write(initial_data)
        f.write(stats_h)
        f.close()

        f = open(save_path_t, 'w')
        f.write(initial_data)
        f.write(stats_t)
        f.close()

        print("\nРезультаты сохранены в \n" + save_path_h + "\n" +
              save_path_t + "\n")

    def calc_stats(self,
                   initial_files: list[str],
                   save_file_name_h='',
                   save_file_name_t='') -> None:
        """Если не задать имена выходных файлов, то генерируются автоматически"""
        stats_h = ''
        stats_t = ''
        num_files = len(initial_files)
        # Упаковка примеров
        for num_file in range(num_files):
            str_stat_h = ''
            str_stat_t = ''
            for eps in self.__list_eps:
                pack = Packing(self.__experiments_dir, "src\\output")
                pack.set_packaging_parameters(0, 0, eps=eps)
                pack.read_polygons_from_file(initial_files[num_file])
                pack.greedy_packing()

                stat = pack.get_stats()
                str_stat_h += str(stat[0]) + ' '
                str_stat_t += str(stat[1]) + ' '

            stats_h += str_stat_h + '\n'
            stats_t += str_stat_t + '\n'

            if num_file == 0:
                time_one_iter = 0
                for timing in str_stat_t.split(' '):
                    if timing != '': time_one_iter += float(timing)
                print("Время одной итерации: ", round(time_one_iter, 3))
                print("Текущее время",
                      time.strftime("%H:%M:%S", time.localtime()))
                print("Прогнозируемое время работы: ",
                      int(time_one_iter * num_files // 60), ":",
                      round(time_one_iter * num_files % 60), "\n")

            print(num_file + 1, '/', num_files)

        self.__save_stats(num_files, stats_h, stats_t, save_file_name_h,
                          save_file_name_t)

        print("Текущее время", time.strftime("%H:%M:%S", time.localtime()))

    def __read_stats(self, file_name: str):
        f = open(self.__results_dir + "\\" + file_name, 'r')
        num_exp = int(f.readline())

        list_eps = f.readline().split(' ')
        epsilons = []
        for j in range(len(list_eps) - 1):  # -1 т.к. строка заканчивается '\n'
            epsilons.append(float(list_eps[j]))
        stats_eps = np.array(epsilons)

        stats_of_exp = np.full((num_exp, len(list_eps) - 1), None)
        for i in range(num_exp):
            list_values = f.readline().split(' ')
            values = []
            for j in range(len(list_values) - 1):
                values.append(float(list_values[j]))
            stats_of_exp[i] = np.array(values)
        f.close()
        return num_exp, stats_eps, stats_of_exp

    def draw_stats(self, file_name: str, is_time_stats=True):
        num_exp, stats_eps, stats_of_exp = self.__read_stats(file_name)

        if is_time_stats:
            ylabel = "Время работы алгоритма"
            expected_label = "Среднее время решения"
            min_max_label = "Max/min время решения"
            save_path = self.__charts_dir + "\\time_stats-"
            save_path += str(calc_num_files(self.__charts_dir) // 2) + ".png"
        else:
            ylabel = "Высота упаковки"
            expected_label = "Средняя высота решения"
            min_max_label = "Max/min высота решения"
            save_path = self.__charts_dir + "\\height_stats-"
            save_path += str(calc_num_files(self.__charts_dir) // 2) + ".png"

        # Настройки вида графика
        fig, ax = plt.subplots()
        xlabel = "Шаг сетки"
        annotations = "Объём выборки: " + str(num_exp)
        settings_function_graph(ax, fig, annotations, xlabel, ylabel)

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


def main() -> None:
    st = Stats()

    # st.create_tests(5, 10, 500, 200)
    
    #  ----------------------------

    # st.append_grid_step(2)
    # st.append_grid_step(4)
    # st.append_grid_step(8)

    # initial_files = []
    # for num_test in range(5):
    #     initial_files.append("test" + str(num_test) + ".txt")

    # st.calc_stats(initial_files)
    
    #  ----------------------------

    st.draw_stats("stats_t-0.txt", is_time_stats=True)
    st.draw_stats("stats_h-0.txt", is_time_stats=False)

if __name__ == "__main__":
    main()