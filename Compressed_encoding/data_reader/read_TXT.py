import numpy as np

def read_TXT(path, packing):
    """Читает многоугольники из txt-файла 
    удаляет дублирующуюся в конец начальную точку если она там есть"""
    f = open(path, 'r')
    num_items = int(f.readline())
    list_pallet_shape = f.readline().split(' ')
    packing.pallet_height = float(list_pallet_shape[0])
    packing.pallet_width = float(list_pallet_shape[1])
    polygons = np.full(num_items, None)
    for i in range(num_items):
        list_points = f.readline().split(' ')
        points = []
        for j in range(0, len(list_points)-1, 2): # -1 т.к. строка заканчивается '\n'
            point = [float(list_points[j]), float(list_points[j+1])]
            points.append(point)
        if (points[0][0] == points[-1][0] and points[0][1] == points[-1][1]):
            points.pop()
        polygons[i] = points
    f.close()
    return polygons

if __name__=='__main__':
    print(read_TXT()[0])
    