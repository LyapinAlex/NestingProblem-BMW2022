import random
from copy import copy

from matplotlib import pyplot as plt, patches


def draw_segments_result_packing(packing):
    pallet_width = packing.pallet_width
    pallet_height = packing.pallet_height
    h = packing.h

    fig, ax = plt.subplots()

    MAX_SIZE = 7
    if pallet_width > pallet_height:
        fig.set_figheight(MAX_SIZE)
        fig.set_figwidth(
            MAX_SIZE * pallet_width / pallet_height)
    else:
        fig.set_figheight(
            MAX_SIZE * pallet_height / pallet_width)
        fig.set_figwidth(MAX_SIZE)

    pallet = patches.Rectangle((0, 0),
                               pallet_width,
                               pallet_height,
                               linewidth=2,
                               facecolor='none',
                               edgecolor='black')
    ax.add_patch(pallet)
    ax.set_xlim(-0.5, pallet_width + 2)
    ax.set_ylim(-0.5, pallet_height + 2)

    for i in range(int(pallet_height / h)):
        plt.plot([0, pallet_width], [i * h, i * h], linestyle='dotted', color='black')

    for polygon in packing.items:
        print(polygon.t_vector)
        i = 0
        while i < len(polygon.points):
            point = copy(polygon.points[i])
            point[0] += polygon.t_vector[0]
            point[1] += polygon.t_vector[1] * h
            polygon.points[i] = copy(point)
            i += 1

        figure = patches.Polygon(polygon.points,
                                 linewidth=1,
                                 edgecolor='red',
                                 fill=False)
        ax.add_patch(figure)
        random_color = "#" + \
                       ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        for i in range(len(polygon.segments)):
            for sigment in polygon.segments[i]:
                sigment[0] += polygon.t_vector[0]
                sigment[1] += polygon.t_vector[0]
                if sigment[0] != sigment[1]:
                    plt.plot(sigment, [(i + polygon.t_vector[1]) * h, (i + polygon.t_vector[1]) * h],
                             color=random_color, alpha=0.7)
                else:
                    ax.scatter(sigment[0], (i + polygon.t_vector[1]) * h, color=random_color, s=4, alpha=0.7)

    plt.savefig('line-packing.png')

    return