from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np
import random


def items2png(path, items, packaging, indent, draw_pixels=False):
    fig, ax = plt.subplots()
    MAX_SIZE = 20
    if packaging.pallet_width > packaging.pallet_height:
        fig.set_figheight(MAX_SIZE * packaging.pallet_height/packaging.pallet_width)
        fig.set_figwidth(MAX_SIZE)
    else:
        fig.set_figheight(MAX_SIZE)
        fig.set_figwidth(MAX_SIZE * packaging.pallet_width/packaging.pallet_height)

    indent = 0
    if packaging.border_distance > packaging.drill_radius:
        indent = packaging.border_distance - packaging.drill_radius
    
    pallet = patches.Rectangle(
        (-indent,-indent), packaging.pallet_width + 2*indent, packaging.pallet_height + 2*indent, linewidth=1, facecolor='none', edgecolor='black')
    ax.add_patch(pallet)

    ax.set_xlim(-indent - packaging.pallet_width*0.015, packaging.pallet_width*1.015 + indent)
    ax.set_ylim(-indent - packaging.pallet_height*0.015, packaging.pallet_height*1.015 + indent)

    for item in items:
        # отрисовка растрового приближения
        if draw_pixels:
            matrix = np.rot90(item.matrix, item.rotation)
            random_color = "#" + \
                ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            for j in range(matrix.shape[1]):
                for i in range(matrix.shape[0]):
                    if matrix[i][j] > 0:
                        sqver = np.array(
                            [[i, j], [i+1, j], [i+1, j+1], [i, j+1]])*packaging.h
                        for i in range(sqver.shape[0]):
                            sqver[i][0] += item.optimal_x
                            sqver[i][1] += item.optimal_y
                        polygon = patches.Polygon(
                            sqver, linewidth=1, facecolor=random_color, edgecolor='black', alpha=0.33)
                        ax.add_patch(polygon)
        # отрисовка предмета
        polygon = patches.Polygon(item.points, linewidth=0.5, edgecolor='red', fill=False)
        ax.add_patch(polygon)

    plt.text(0, (packaging.pallet_height + indent*2)*1.025, packaging.get_annotation(), fontsize=15, color='green')
    plt.savefig(path[:-4] + str(items[0].pallet_id) + '.png')
    return None

