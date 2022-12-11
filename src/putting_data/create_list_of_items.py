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
    Вертикально ориентируем фигуру
    """
    x_max, y_max = np.amax(points, axis=0)
    x_min, y_min = np.amin(points, axis=0)

    if (x_max - x_min < y_max - y_min):
        for point in points:
            point0_copy = point[0]
            point[0] = -point[1]
            point[1] = point0_copy
    return None


def create_size(radius):
    size = random.uniform(0,100)
    if size<75:
        avg_radius = random.uniform(radius / 27, radius / 15)
    elif size<96:
        avg_radius = random.uniform(radius / 9.5, radius / 8)
    elif size<100:
        avg_radius = random.uniform(radius / 6.6, radius / 5.5)
    return avg_radius*1.8


def create_list_of_items(num_items, max_width=20, max_height=20):
    """
    Создание массива вертикально ориентированных объектов без растрового представления
    """
    radius = min(max_width, max_height) / 2

    data = np.full(num_items, None)
    for id in range(num_items):  
        # здесь потом можно будет добавить круги и т.д.
        num_corners = random.randint(30, 50)
        points = generate_polygon(
            center=(100, 100),
            avg_radius=create_size(radius),
            irregularity=0.05,  # отступ между "центрами"
            spikiness=0.3,  # радиус "вогнутости"
            num_vertices=num_corners)
        rotation(points)
        size = shift2zero(points)

        data[id] = points
    return data


def draw_polygon(points):
    fig, ax = plt.subplots()

    MAX_SIZE = 3
    fig.set_figheight(MAX_SIZE)
    fig.set_figwidth(MAX_SIZE)

    MAX_SIZE_LIM = np.amax(points)
    ax.set_xlim(-0.5, MAX_SIZE_LIM + 0.5)
    ax.set_ylim(-0.5, MAX_SIZE_LIM + 0.5)

    polygon = patches.Polygon(points, linewidth=1, edgecolor='red', fill=False)
    ax.add_patch(polygon)
    plt.show()
    return None


if __name__ == "__main__":
    li = create_list_of_items(3)
    for p in li:
        draw_polygon(p)