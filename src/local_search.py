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

def packing_from_swim(input_file_name: str,
                      width=10000,
                      height=5752):
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
    return packaging

def write_packaging(packaging: Packing, output_file_name: str):
    packaging.print_stats()
    packaging.change_position()
    packaging.save_pallets_in_files(output_file_name)

def local_search(packaging: Packing, neighborhood: int):
    packaging.greedy_packing()
    target_value = packaging.get_stats()[0]
    target_sequence = packaging.items.copy()
    for i in range(packaging.num_items-1):
        for j in range(i+1, i+neighborhood):
            if j > packaging.num_items-1:
                continue
            packaging.swap_itemes(i, j)
            packaging.greedy_packing()
            value = packaging.get_stats()[0]
            if target_value > value:
                target_value = value
                swap_pair = (i, j)
                target_sequence = packaging.items.copy()
            packaging.swap_itemes(i, j)
            print(j, ":", target_value, ":", value)
        print("---------------===============---------------")

    print("swap_pair =", swap_pair)
    return target_sequence

def main():
    # ----------- начальные данные -----------
    dirict = "special_tests"
    input_file_name = "test_zero.txt"
    eps = 1
    neighborhood = 50

    # --------- настройка упаковщика ---------
    packaging = read_our_tests(input_file_name, "src\\input\\"+dirict+"\\")
    # packaging = packing_from_swim(input_file_name="swim.txt")
    packaging.make_items(h = eps, num_rout = 4)
    packaging.sort_items(num_sort = 2)

    # ----------- локальный поиск ------------
    packaging.swap_itemes(0, 12)

    start_t = time.time()
    packaging.items = local_search(packaging, neighborhood)
    end_t = time.time()
    print("\n",end_t - start_t)
    
    packaging.greedy_packing()
    write_packaging(packaging, "swim-LS2.png")


if __name__ == '__main__':
    main()