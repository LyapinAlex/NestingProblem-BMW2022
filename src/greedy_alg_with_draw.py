from data_rendering.polygons2txt import polygons2txt
from data_rendering.items2txt import items2txt
from class_packing import Packing

def main():
    # Начальные данные
    pallet_width = 2000
    pallet_height = 1000
    drill_radius = 0

    packaging = Packing(pallet_width, pallet_height, drill_radius)
    num_items = 150
    file_name = None
    # file_name = r'src/input/NEST001-108.DXF'
    # file_name = r'src/input/NEST002-216.svg'
    # file_name = r'src/input/NEST003-432.svg'

    # Инициализация предметов
    if file_name == None:
        packaging.create_random_polygons(num_items)
    else:
        packaging.read_polygons_from_file(file_name)

    # Жадный алгоритм
    packaging.make_items()
    packaging.sort_items()
    packaging.greedy_packing()

    # polygons2txt(polygons, path=r'src\output\polygons' + str(len(polygons)) + '.txt')
    # items2txt(packaging.items, path=r'src\output\items'+str(len(polygons))+'.txt')

    # Результаты упаковки
    packaging.print_stats()
    packaging.draw_solution()
    return None


if __name__ == '__main__':
    main()
