import numpy as np

def shift2zero(points):
    x_max, y_max = np.amax(points, axis = 0)
    x_min, y_min = np.amin(points, axis = 0)
    # сдвиг фигуры к началу координат

    for i in range(0, (points).shape[0]):
        points[i][0] -= x_min
        points[i][1] -= y_min
    return [x_max - x_min, y_max - y_min]
