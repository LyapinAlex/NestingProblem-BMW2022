def items2txt(path, items, duplicate_first_point_to_end=True, is_in_one_file = False):
    """Создаёт файл содержащий многоугольники из массива"""
    if is_in_one_file:
        f = open(path, 'w')
    else:
        f = open(path[:-4] + str(items[0].pallet_id) + '.txt', 'w')
    f.write(str(len(items)) + '\n')
    # f.write(str(210) + " " + str(100) + '\n')
    for item in items:
        s = ''
        for point in item.points:
            s += str(point[0]) + ' ' + str(point[1]) + ' '
        if duplicate_first_point_to_end:
            f.write(s + str(item.points[0][0]) + ' ' + str(item.points[0][1]) + '\n')
        else:
            f.write(s + '\n')
    f.close()
