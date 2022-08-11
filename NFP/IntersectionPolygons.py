from NFP.IntersectionPoint import intersection_point


def intersection_polygon_by_edge(item, edge):
    points = []
    # print(item[0].coordinate[0])
    for vertex in item:
        point = False
        # можно улучшить написав условия, когда может пересекаться
        # if (np.min([vertex.coordinate[0], vertex.edges[0][0]]) > np.max([edge.coordinate[0], edge.edges[0][0]])) or (np.max([vertex.coordinate[0], vertex.edges[0][0]]) < np.min([edge.coordinate[0], edge.edges[0][0]])) or not(
        #     np.min([vertex.coordinate[1], vertex.edges[0][1]]) > np.max([edge.coordinate[1], edge.edges[0][1]])) or ( np.max([vertex.coordinate[1], vertex.edges[0][1]]) < np.min([edge.coordinate[1], edge.edges[0][1]])):
        #     print('здесь')
        #     point = intersection_point(vertex, edge)
        #     points.append(point)
        point = intersection_point(vertex, edge)
        if point:
            points.append(point)
    if points:
        return points
    else:
        return False
