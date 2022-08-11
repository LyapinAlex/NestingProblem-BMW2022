from NFP.IntersectionPoint import intersection_point


def intersection_polygon_by_edge(item, edge):
    points = []
    for vertex in item:
        point = False
        if not (vertex.coordinate[0] > edge.coordinate[0] and vertex.edges[0][0] > edge.coordinate[0]
                        and vertex.coordinate[0] > edge.edges[0][0] and vertex.edges[0][0] > edge.edges[0][0]) and not (
                vertex.coordinate[0] < edge.coordinate[0] and vertex.edges[0][0] < edge.coordinate[0]
                        and vertex.coordinate[0] < edge.edges[0][0] and vertex.edges[0][0] < edge.edges[0][0]) and not (
                vertex.coordinate[1] > edge.coordinate[1] and vertex.edges[0][1] > edge.coordinate[1]
                        and vertex.coordinate[1] > edge.edges[0][1] and vertex.edges[0][1] > edge.edges[0][1]) and not (
                vertex.coordinate[1] < edge.coordinate[1] and vertex.edges[0][1] < edge.coordinate[1]
                        and vertex.coordinate[1] < edge.edges[0][1] and vertex.edges[0][1] < edge.edges[0][1]):
            print('здесь')
            point = intersection_point(vertex, edge)
            points.append(point)
    if points:
        return points
    else:
        return False
