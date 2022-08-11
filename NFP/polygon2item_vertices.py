import numpy as np

if __name__=='__main__':
    from classes import Vertex
    from generators.generate_polygon1 import generate_polygon
else:
    from .classes import Vertex
    from .generators.generate_polygon1 import generate_polygon

def polygon2item_vertices(points):
    """
    Args:
        points(np.array):
            набор точек
    Returns:
        np.array[vertex]
    """
    p1 = 0
    y_min = points[0][1]
    x_min = points[0][0]
    for i in range(1, (points).shape[0]):
        if ( points[i][1] < y_min ) or ( points[i][1] == y_min and points[i][0] < x_min ): 
            p1 = i
            y_min = points[i][1]
            x_min = points[i][0]
    p2 = (p1 + 1) % points.shape[0]
    p0 = (p1 - 1) % points.shape[0]
# отнормировать вектора из p1
# сравнить по первым координатам -> понять где внутренность
# создать вектор поворота для определения нормали
    item_vertices = []
    ver1 = Vertex(points[points.shape[0]-1])
    item_vertices.append(ver1)
    for i in range(points.shape[0] - 2, -1, -1):
        ver0 = Vertex(points[i], [[ver1, np.array([0,0])]])
        ver1 = ver0
        item_vertices.append(ver1)
    item_vertices[0].append_vertex(ver1)

    item_vertices = sorted(item_vertices, key=lambda x: x.coordinate[0])

    # for i in item_vertices:
    #     print(i.coordinate)

    # v = item_vertices[0]
    # for i in range(0, points.shape[0]):
    #     v.coordinate = np.array([0,0])
    #     v = v.get_neighboring_vertex()
    
    return np.array(item_vertices)

if __name__=='__main__':
    polygon2item_vertices(generate_polygon(center=(250, 250), avg_radius=100, irregularity=0.35, spikiness=0.2, num_vertices=6))