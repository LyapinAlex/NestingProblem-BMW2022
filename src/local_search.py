from class_packing import Packing
from class_item import Item
import numpy as np
import time


def read_our_tests(input_file_name: str,
                           input_dir="src\\input\\concave50\\"):
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
    return packaging


def write_packaging(packaging: Packing, output_file_name: str):
    packaging.print_stats()
    packaging.change_position()
    packaging.save_pallets_in_files(output_file_name)


def local_search(packaging: Packing, neighborhood: int):
    packaging.greedy_packing()
    target_value = packaging.get_stats()[0]
    target_sequence = packaging.items.copy()
    for i in range(packaging.num_items):
        for j in range(i+1, i+neighborhood):
            if j > packaging.num_items-1:
                continue
            packaging.swap_itemes(i,j)
            packaging.greedy_packing()
            value = packaging.get_stats()[0]
            if target_value > value:
                target_value = value
                target_sequence = packaging.items.copy()
            packaging.swap_itemes(i,j)
        print(i, ":", target_value)

    packaging.items = target_sequence
    packaging.greedy_packing()
    write_packaging(packaging, "test_zero-LS.png")


def main():
    # ----------- начальные данные -----------
    dirict = "special_tests"
    input_file_name = "test_zero.txt"
    eps = 1
    neighborhood = 50

    # --------- настройка упаковщика ---------
    packaging = read_our_tests(input_file_name, "src\\input\\"+dirict+"\\")
    packaging.make_items(h = eps, num_rout = 4)
    packaging.sort_items(num_sort = 2)

    # ----------- локальный поиск ------------
    start_t = time.time()
    local_search(packaging, neighborhood)
    print("\n",time.time() - start_t)
    
    # packaging.swap_itemes(0,7)
    # packaging.swap_itemes(0,14)
    # packaging.swap_itemes(10,16)
    # packaging.swap_itemes(10,15)
    # packaging.swap_itemes(5,11)
    # packaging.greedy_packing()
    # write_packaging(packaging, "test0-LS4.png")


if __name__ == '__main__':
    main()