def save_raw_data(path, packing):
    """Создаёт txt-файл содержащий сырые (необработанные) данные\\
    В первой строке файла формата .txt записывается единственное целое число N – количество упаковываемых многоугольников.\\
    Вторая строка содержит два числа: высоту и ширину листа на котором будут размещаться многоугольники.\\
    В каждой из N следующих строк содержатся координаты вершин упаковываемых многоугольников: x1 y1 x2 y2 x3 y3 ... xM yM. Если соединить точки в данном порядке, а также первую и последнюю точки, получится заданный многоугольник."""
    f = open(path, 'w')
    f.write(str(packing.num_items) + '\n')
    f.write(str(packing.pallet_height) + " " + str(packing.pallet_width) + '\n')
    for item in packing.items:
        for _ in range(item.num_copies):
            s = ''
            for point in item.original_polygon.points:
                s += str(point.x) + ' ' + str(point.y) + ' '
            f.write(s + '\n')
    f.close()
