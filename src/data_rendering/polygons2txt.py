def polygons2txt(polygons,
             path='src\output\polygons.txt',
             duplicate_first_point_to_end=True):
    """Создаёт файл содержащий многоугольники из массива"""
    f = open(path, 'w')
    f.write(str(len(polygons)) + '\n')
    for polygon in polygons:
        s = ''
        for point in polygon:
            s += str(point[0]) + ' ' + str(point[1]) + ' '
        if duplicate_first_point_to_end:
            f.write(s + str(polygon[0][0]) + ' ' + str(polygon[0][1]) + '\n')
        else:
            f.write(s + '\n')
    f.close()
