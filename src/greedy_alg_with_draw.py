from class_packing import Packing


def main():
    # Начальные данные
    packaging = Packing(width=2000, height=1000, drill_radius=2, border_distance=2.1)
    # Инициализация предметов
    num_items = 100
    file_name = None
    # file_name = r'NEST001-108.dxf'
    # file_name = r'NEST002-216.dxf'
    file_name = r'NEST003-432.dxf'
    # file_name = r"items401.txt"
    if file_name == None:
        packaging.create_random_polygons(num_items)
    else:
        packaging.read_polygons_from_file(file_name)

    eps = 5.75/4
    # Жадный алгоритм
    packaging.make_items(h = eps, num_rout=3)
    # packaging.save_items_in_file('items' + str(packaging.num_items) + '.txt')

    num_sort = 2
    packaging.sort_items(num_sort=num_sort)
    packaging.greedy_packing()

    # Результаты упаковки
    packaging.print_stats()
    # packaging.clear_output()

    packaging.change_position()
    # packaging.save_pallets_in_files('pallet.dxf')
    # packaging.save_pallets_in_files('pallet.txt')
    packaging.save_pallets_in_files('pa'+str(num_sort)+'.svg')
    packaging.save_pallets_in_files('pa'+str(num_sort)+'.png')
    return None


if __name__ == '__main__':
    main()
