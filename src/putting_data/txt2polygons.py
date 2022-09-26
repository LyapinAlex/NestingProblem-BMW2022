import numpy as np

def txt2polygons(path=r'src\input\test0.txt'):
    """Создаёт файл содержащий многоугольники из массива"""
    f = open(path, 'r')
    num_items = int(f.readline())
    polygons = np.full(num_items, None)
    for i in range(num_items):
        list_points = f.readline().split(' ')
        list_points.pop()
        points= []
        for j in range(0, len(list_points), 2):
            point = [float(list_points[j]), float(list_points[j+1])]
            points.append(point)
        polygons[i] = np.array(points)
    f.close()
    return polygons

if __name__=='__main__':
    print(txt2polygons())
    