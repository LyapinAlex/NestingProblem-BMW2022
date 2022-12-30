import random
import numpy as np
from matplotlib import patches
from matplotlib import pyplot as plt


def image_size(fig, size, MAX_SIZE=5):
    if size.x > size.y:
        fig.set_figheight(MAX_SIZE)
        fig.set_figwidth(MAX_SIZE * size.x / size.y)
    else:
        fig.set_figheight(MAX_SIZE * size.y / size.x)
        fig.set_figwidth(MAX_SIZE)

    fig.set_figheight(MAX_SIZE)
    fig.set_figwidth(MAX_SIZE)


def focusing_on_subject(ax, minXY, maxXY):
    """Задаёт облатсь отображаемую на рисунке, где \\
        minXY - координата левого нижнего угла, отображемой прямоугольной области, \\
        maxXY - правого верхнего угла"""
    INDENT_X = (maxXY.x - minXY.x) * 0.1
    INDENT_Y = (maxXY.y - minXY.y) * 0.1
    ax.set_xlim(minXY.x - INDENT_X, maxXY.x + INDENT_X)
    ax.set_ylim(minXY.y - INDENT_Y, maxXY.y + INDENT_Y)


def draw_polygon(ax, polygon, edgecolor='red'):
    ax.add_patch(
        patches.Polygon(polygon.points_to_list(),
                        linewidth=1,
                        edgecolor=edgecolor,
                        fill=False))


def draw_raster_approximation(ax, polygon_minXY, matrix, h, is_random_color=False):
    move_matrix = np.full((4, 2), [polygon_minXY.x, polygon_minXY.y])
    if is_random_color:
        color = "#" + ''.join(
            [random.choice('0123456789ABCDEF') for j in range(6)])
    else:
        color = 'silver'

    for i in range(matrix.shape[1]):
        for j in range(matrix.shape[0]):
            if matrix[j][i]:
                sqver = np.array([[i, j], [i + 1, j], [i + 1, j + 1],
                                  [i, j + 1]]) * h + move_matrix
                polygon = patches.Polygon(sqver,
                                          linewidth=1,
                                          facecolor=color,
                                          edgecolor='black',
                                          alpha=0.33)
                ax.add_patch(polygon)


def draw_compressed_encoding(ax,
                             polygon_minXY,
                             compressed_encoding,
                             h,
                             vector = None,
                             is_random_color=False):
    if not vector is None:
        move_matrix = np.full((4, 2), [polygon_minXY.x - vector.x, polygon_minXY.y - vector.y])
    else:
        move_matrix = np.full((4, 2), [polygon_minXY.x, polygon_minXY.y])

    if is_random_color:
        color = "#" + ''.join(
            [random.choice('0123456789ABCDEF') for j in range(6)])
    else:
        color = 'silver'

    for num_line in range(compressed_encoding.shape[0]):
        indent = 0
        for num_unite in range(len(compressed_encoding[num_line])):
            if compressed_encoding[num_line][num_unite] > 0:
                length = compressed_encoding[num_line][num_unite]
                sqver = np.array([[indent, num_line], [indent + length, num_line],
                                  [indent + length, num_line + 1],
                                  [indent, num_line + 1]]) * h + move_matrix
                poly = patches.Polygon(sqver,
                                          linewidth=1,
                                          facecolor=color,
                                          edgecolor='black',
                                          alpha=0.33)
                ax.add_patch(poly)
            indent += abs(compressed_encoding[num_line][num_unite])