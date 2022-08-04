from matplotlib import pyplot as plt
from matplotlib import patches

def draw_pallet(items, pallet_width, pallet_height):
    fig, ax = plt.subplots()
    pallet = patches.Rectangle((0, 0), pallet_width, pallet_height, linewidth=2, facecolor='none', edgecolor='black')
    ax.add_patch(pallet)
    ax.set_xlim(-1, pallet_width + 1)
    ax.set_ylim(-1, pallet_height + 1)
    for item in items:
        for point in item.points:
            point[0] += item.lb_x
            point[1] += item.lb_y
        polygon = patches.Polygon(item.points, linewidth=1, facecolor='silver', edgecolor='black')
        ax.add_patch(polygon)
    return fig, ax

def draw_all_pallets(packing, pallet_width, pallet_leight):
    for i in range(len(packing)):
        draw_pallet(packing[i], pallet_width, pallet_leight)