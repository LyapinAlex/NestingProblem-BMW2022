from class_packing import Packing


def main():
    # Начальные данные
    packaging = Packing(width=2000, height=1000, drill_radius=0)
    # Инициализация предметов
    num_items = 401
    file_name = None
    file_name = r'NEST001-108.dxf'
    # file_name = r'NEST002-216.svg'
    # file_name = r'NEST003-432.svg'
    file_name = r"items401.txt"
    if file_name == None:
        packaging.create_random_polygons(num_items)
    else:
        packaging.read_polygons_from_file(file_name)

    # Жадный алгоритм

    packaging.make_items()
    # packaging.save_items_in_file('items' + str(packaging.num_items) + '.txt')
    packaging.sort_items()
    packaging.greedy_packing()

    # Результаты упаковки

    packaging.print_stats()
    packaging.change_position()

    packaging.clear_output()
    # packaging.save_pallets_in_files('pallet.dxf')
    # packaging.save_pallets_in_files('pallet.txt')
    packaging.save_pallets_in_files('pallet.png')
    return None


if __name__ == '__main__':
    main()
