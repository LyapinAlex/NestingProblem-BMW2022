import math
import random
import numpy as np
from matplotlib import patches
from matplotlib import pyplot as plt
from class_polygon import Polygon


def drow_rastr_apr(ax, polygon, h):
    matrix = polygon.create_rastr_approximation(h)
    move_matrix = np.full((4, 2), [polygon.minXY().x, polygon.minXY().y])
    random_color = "#" + \
        ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    random_color = 'silver'
    for i in range(matrix.shape[1]):
        for j in range(matrix.shape[0]):
            if matrix[j][i]:
                sqver = np.array([[i, j], [i + 1, j], [i + 1, j + 1],
                                  [i, j + 1]]) * h + move_matrix
                poly = patches.Polygon(sqver,
                                       linewidth=1,
                                       facecolor=random_color,
                                       edgecolor='black',
                                       alpha=0.33)
                ax.add_patch(poly)


def draw(polygon: Polygon,
         indent_expand_polygon=0.5,
         is_draw_raster_approximation=False,
         h=None):

    # ----------   background   ----------

    fig, ax = plt.subplots()
    MAX_SIZE = 4
    polygon.resize()
    if polygon.size.x > polygon.size.y:
        fig.set_figheight(MAX_SIZE)
        fig.set_figwidth(MAX_SIZE * polygon.size.x / polygon.size.y)
    else:
        fig.set_figheight(MAX_SIZE * polygon.size.y / polygon.size.x)
        fig.set_figwidth(MAX_SIZE)

    fig.set_figheight(MAX_SIZE)
    fig.set_figwidth(MAX_SIZE)

    INDENT = 5
    ax.set_xlim(polygon.minXY().x - INDENT, polygon.maxXY().x + INDENT)
    ax.set_ylim(polygon.minXY().y - INDENT, polygon.maxXY().y + INDENT)

    # ----------   draw polygon and other   ----------

    circumscribed_rectangle = patches.Rectangle(polygon.minXY().to_tuple(),
                                                polygon.size.x,
                                                polygon.size.y,
                                                linewidth=2,
                                                facecolor='none',
                                                edgecolor='black')
    ax.add_patch(circumscribed_rectangle)

    if is_draw_raster_approximation:
        drow_rastr_apr(ax, polygon, h)

    poly = patches.Polygon(polygon.points_to_list(),
                           linewidth=1,
                           edgecolor='red',
                           fill=False)
    ax.add_patch(poly)

    exp_polygon = patches.Polygon(
        polygon.expand_polygon(indent_expand_polygon).points_to_list(),
        linewidth=1,
        edgecolor='green',
        fill=False)
    ax.add_patch(exp_polygon)

    bar = polygon.calc_centroid()
    plt.plot(bar.x, bar.y, 'co')
    plt.show()


if __name__ == '__main__':
    list_points = [[592.205, 683.901], [593.992, 680.914], [594.958, 680.656],
                   [596.495, 679.457], [596.705, 677.52], [577.463, 644.192],
                   [575.68, 643.405], [573.874, 644.137], [573.167, 644.845],
                   [569.687, 644.898], [538.79, 627.06], [537.097, 624.02],
                   [537.356, 623.054], [537.087, 621.123], [535.514, 619.973],
                   [497.03, 619.973], [495.457, 621.123], [495.188, 623.053],
                   [495.447, 624.02], [493.754, 627.06], [462.857, 644.898],
                   [459.377, 644.844], [458.67, 644.138], [456.864, 643.405],
                   [455.081, 644.192], [435.839, 677.52], [436.049, 679.457],
                   [437.586, 680.655], [438.553, 680.915], [440.339, 683.901],
                   [440.339, 719.577], [438.553, 722.564], [437.586, 722.824],
                   [436.049, 724.021], [435.839, 725.959], [455.081, 759.286],
                   [456.864, 760.073], [458.67, 759.341], [459.377, 758.634],
                   [462.857, 758.58], [493.754, 776.418], [495.447, 779.459],
                   [495.188, 780.426], [495.457, 782.355], [497.03, 783.506],
                   [535.514, 783.506], [537.087, 782.355], [537.356, 780.425],
                   [537.097, 779.459], [538.79, 776.418], [569.687, 758.58],
                   [573.167, 758.634], [573.874, 759.342], [575.68, 760.073],
                   [577.463, 759.286], [596.705, 725.959], [596.495, 724.021],
                   [594.958, 722.823], [593.992, 722.565], [592.205, 719.577],
                   [592.205, 683.9]]
    pol1 = Polygon(list_points)
    draw(pol1, is_draw_raster_approximation=True, h=10)
