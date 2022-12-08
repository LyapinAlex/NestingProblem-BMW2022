import numpy as np
from class_packing import Packing
from class_item import Item

# Датасеты: https://www.euro-online.org/websites/esicup/data-sets/

def packing_from_our_tests(input_file_name: str,
                            input_dir = "src\\input\\tests\\",
                            output_file_name='',
                            num_rot=4,
                            num_sort=2,
                            eps=0.0):
    """Входные данные типа test1"""
    path = input_dir + input_file_name
    f = open(path, 'r')
    num_items = int(f.readline())
    polygons = np.full(num_items, None)
    list_pallet_shape = f.readline().split(' ')
    for i in range(num_items):
        list_points = f.readline().split(' ')
        points = []
        for j in range(0, len(list_points)-1, 2):
            point = [float(list_points[j]), float(list_points[j+1])]
            points.append(point)
        if (points[0][0] == points[-1][0] and points[0][1] == points[-1][1]):
            points.pop()
        polygons[i] = np.array(points)
    f.close()
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

    packaging.make_items(h=eps, num_rout=num_rot)
    packaging.sort_items(num_sort=num_sort)
    packaging.greedy_packing()
    packaging.print_stats()
    packaging.change_position()
    if output_file_name=='':
        output_file_name = input_file_name[0:-3]+'png'
    packaging.save_pallets_in_files(output_file_name)
    return packaging.get_stats()


def packing_from_Terashima2(input_file_name: str,
                            output_file_name='',
                            num_rot=4,
                            num_sort=2,
                            eps=0.0):
    """Входные данные типа Terashima2 (распаковываем интересующие файлы и запускаем)"""
    # ------------  чтение файла  ------------
    path = "src\\input\\" + input_file_name
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
    # ------------  Упаковка  ------------
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

    packaging.make_items(h=eps, num_rout=num_rot)
    packaging.sort_items(num_sort=num_sort)
    packaging.greedy_packing()
    packaging.print_stats()
    packaging.change_position()
    if output_file_name=='':
        output_file_name = input_file_name[0:-3]+'png'
    packaging.save_pallets_in_files(output_file_name)
    return packaging.get_stats()


def packing_from_swim(input_file_name: str,
                      output_file_name = '',
                      width=10000,
                      height=5752,
                      num_rot=0,
                      num_sort=0,
                      eps=0.0):
    """Входные данные типа swim.txt (trousers.txt)"""
    # ------------  чтение файла  ------------
    path = "src\\input\\" + input_file_name
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
    # ------------  Упаковка  ------------
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
    packaging.make_items(h=eps, num_rout=num_rot)
    packaging.sort_items(num_sort=num_sort)
    packaging.greedy_packing()
    packaging.print_stats()
    packaging.change_position()
    if output_file_name=='':
        output_file_name = input_file_name[0:-3]+'png'
    packaging.save_pallets_in_files(output_file_name)
    return packaging.get_stats()


def create_pack(output_file_name: str):
    packaging = Packing(width=1500,
                        height=1500,
                        drill_radius=0,
                        border_distance=0)
    packaging.create_random_polygons(50)
    packaging.output_dir = "src\\input\\tests"
    packaging.save_items_in_file(output_file_name, False)
    return


if __name__ == '__main__':
    for i in range(0,10):
        create_pack('test'+str(i)+'.txt')
        # packing_from_our_tests(input_file_name='test'+str(i)+'.txt')
    # packing_from_swim('swim.txt', eps=36/2)
    # packing_from_swim('trousers.txt', width=500, height=79)
    # packing_from_our_tests(input_file_name='my_test1.txt', input_dir = "src\\input\\special_tests\\")