import numpy as np
import random
from matplotlib import pyplot as plt
from matplotlib import patches

if __name__ == '__main__':
    from generate_polygon1 import generate_polygon
else:
    from .generate_polygon1 import generate_polygon


def shift2zero(points):
    x_max, y_max = np.amax(points, axis=0)
    x_min, y_min = np.amin(points, axis=0)
    # сдвиг фигуры к началу координат

    for i in range(0, (points).shape[0]):
        points[i][0] -= x_min
        points[i][1] -= y_min
    return [x_max - x_min, y_max - y_min]


def rotation(points):
    """
    Приводим фигуру к вертикальному виду
    """
    x_max, y_max = np.amax(points, axis=0)
    x_min, y_min = np.amin(points, axis=0)

    if (x_max - x_min > y_max - y_min):
        for point in points:
            point0_copy = point[0]
            point[0] = -point[1]
            point[1] = point0_copy

    shift2zero(points)
    return None


def create_list_of_items(num_items):
    """
    Создание массива необработанных объектов
    """
    data = np.full(num_items, None)
    for id in range(num_items): # здесь потом можно будет добавить круги и т.д.
        num_corners = random.randint(3, 8)
        points = generate_polygon(center=(100, 100),
                                  avg_radius=100,
                                  irregularity=0.5,
                                  spikiness=0.75,
                                  num_vertices=num_corners)
        rotation(points)
        data[id] = points
    return data


def draw_polygon(points):
    fig, ax = plt.subplots()

    MAX_SIZE = 3
    fig.set_figheight(MAX_SIZE)
    fig.set_figwidth(MAX_SIZE)

    MAX_SIZE1 = np.amax(points)
    ax.set_xlim(-1, MAX_SIZE1 + 1)
    ax.set_ylim(-1, MAX_SIZE1 + 1)

    polygon = patches.Polygon(points, linewidth=1, edgecolor='red', fill=False)
    ax.add_patch(polygon)
    plt.show()
    return None


if __name__ == "__main__":
    li = create_list_of_items(2)
    for p in li:
        draw_polygon(p)