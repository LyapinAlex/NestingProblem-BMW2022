def items2txt(items,
             path='src\output\items.txt',
             duplicate_first_point_to_end=True):
    """Создаёт файл содержащий многоугольники из массива"""
    f = open(path, 'w')
    f.write(str(len(items)) + '\n')
    for item in items:
        s = ''
        for point in item.points:
            s += str(point[0]) + ' ' + str(point[1]) + ' '
        if duplicate_first_point_to_end:
            f.write(s + str(item.points[0][0]) + ' ' + str(item.points[0][1]) + '\n')
        else:
            f.write(s + '\n')
    f.close()