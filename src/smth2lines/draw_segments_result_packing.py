from copy import copy

from matplotlib import pyplot as plt, patches


def draw_segments_result_packing(packing):

    pallet_width = packing.pallet_width
    pallet_height = packing.pallet_height
    h = packing.h
    items = packing.items

    fig, ax = plt.subplots()

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

    for polygon in items:
        print(polygon.t_vector)
        for point in polygon.points:
            point[0] += polygon.t_vector[0]
            point[1] += polygon.t_vector[1]
        figure = patches.Polygon(polygon.points,
                                 linewidth=1,
                                 edgecolor='red',
                                 fill=False)
        ax.add_patch(figure)

    plt.savefig('line-packing.png')
