import numpy as np

def txt2polygons(path=r'src\input\test0.txt'):
    """Создаёт файл содержащий многоугольники из массива 
    удаляет дублирующуюся в конец начальную точку если она там есть"""
    f = open(path, 'r')
    num_items = int(f.readline())
    polygons = np.full(num_items, None)
    for i in range(num_items):
        list_points = f.readline().split(' ')
        points = []
        for j in range(0, len(list_points)-1, 2): # -1 т.к. строка заканчивается '\n'
            point = [float(list_points[j]), float(list_points[j+1])]
            points.append(point)
        if (points[0][0] == points[-1][0] and points[0][1] == points[-1][1]):
            points.pop()
        polygons[i] = np.array(points)
    f.close()
    return polygons

if __name__=='__main__':
    print(txt2polygons()[0])
    