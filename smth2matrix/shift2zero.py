def shift2zero(points):
    # сдвиг фигуры к началу координат
    x_max = max(points[0][0], points[1][0])
    x_min = min(points[0][0], points[1][0])
    y_max = max(points[0][1], points[1][1])
    y_min = min(points[0][1], points[1][1])
    for i in range(0, (points).shape[0]):
        x_max = max(x_max, points[i][0])
        y_max = max(y_max, points[i][1])
        x_min = min(x_min, points[i][0])
        y_min = min(y_min, points[i][1])
    # нормировка фигуры к (0,0)
    for i in range(0, (points).shape[0]):
        points[i][0] -= x_min
        points[i][1] -= y_min
    return [x_max - x_min, y_max - y_min]