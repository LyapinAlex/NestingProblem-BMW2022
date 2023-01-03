def save_pallet_as_TXT(path, pallet):
    """Создаёт файл содержащий многоугольники из массива"""
    f = open(path[:-4] + '-' + str(pallet.id) + '.txt', 'w')
    f.write(str(pallet.num_plased_items) + '\n')
    f.write(str(pallet.height) + " " + str(pallet.width) + '\n')
    for position in pallet.plased_items_positions:
        points = position.polygon_on_position.points_to_list()
        s = ''
        for point in points:
            s += str(point[0]) + ' ' + str(point[1]) + ' '
        f.write(s + '\n')
    f.close()


def save_as_TXT(path, packing) -> None:
    for pallet in packing.pallets:
        save_pallet_as_TXT(path, pallet)