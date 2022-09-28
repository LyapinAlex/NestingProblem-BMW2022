from matplotlib import pyplot as plt
from matplotlib import patches


def drow_pallet_with_polygons(polygons, pallet_width, pallet_height, path = r'src\output\pallet_from_cpp.png'):
    fig, ax = plt.subplots()
    MAX_SIZE = 20
    if pallet_width > pallet_height:
        fig.set_figheight(MAX_SIZE * pallet_height / pallet_width)
        fig.set_figwidth(MAX_SIZE)
    else:
        fig.set_figheight(MAX_SIZE)
        fig.set_figwidth(MAX_SIZE * pallet_width / pallet_height)

    pallet = patches.Rectangle((0, 0),
                               pallet_width,
                               pallet_height,
                               linewidth=2,
                               facecolor='none',
                               edgecolor='black')
    ax.add_patch(pallet)
    ax.set_xlim(-0.5, pallet_width + 2)
    ax.set_ylim(-0.5, pallet_height + 2)

    for polygon in polygons:
        figure = patches.Polygon(polygon,
                                 linewidth=1,
                                 edgecolor='red',
                                 fill=False)
        ax.add_patch(figure)

    plt.savefig(path)
    return None