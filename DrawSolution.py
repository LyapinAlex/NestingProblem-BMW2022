from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np
import math

def draw_pallet(items, pallet_width, pallet_height, h):
    fig, ax = plt.subplots()
    MAX_SIZE = 20
    if pallet_width > pallet_height:
        fig.set_figheight(MAX_SIZE * pallet_height/pallet_width)
        fig.set_figwidth(MAX_SIZE)
    else:
        fig.set_figheight(MAX_SIZE)
        fig.set_figwidth(MAX_SIZE * pallet_width/pallet_height)

   
    pallet = patches.Rectangle((0, 0), pallet_width, pallet_height, linewidth=2, facecolor='none', edgecolor='black')
    ax.add_patch(pallet)
    ax.set_xlim(-0.5, pallet_width + 2)
    ax.set_ylim(-0.5, pallet_height + 2)

    for item in items:

        r = int(item.rotation*2 / math.pi)
        item.surfPoint()
        
        for point in item.points:

            point0_copy = point[0]
            point1_copy = point[1]
            if r == 0:
                continue
            if r == 1:

                point[0] = -point1_copy
                point[1] = point0_copy

            if r == 2:
                point[0] = -point0_copy
                point[1] = -point1_copy
            if r == 3:

                point[0] = point1_copy
                point[1] = -point0_copy

        for point in item.points:

            
            if r == 0:
                point[0] += item.lb_x
                point[1] += item.lb_y
            if r == 1:

                point[0] += item.lb_x + h*len(item.matrix[0])
                point[1] += item.lb_y

            if r == 2:
                point[0] += item.lb_x + h*len(item.matrix)
                point[1] += item.lb_y + h*len(item.matrix[0])
            if r == 3:

                point[0] += item.lb_x
                point[1] += item.lb_y + h*len(item.matrix)

      




        # for point in item.points:
        #     point0_copy = point[0]
        #     point[0] = math.cos(item.rotation)*point[0] - math.sin(item.rotation)*point[1]
        #     point[1] = math.sin(item.rotation)*point0_copy + math.cos(item.rotation)*point[1]
        
        # item.surfPoint()
        # for point in item.points:
        #     point[0] += item.lb_x
        #     point[1] += item.lb_y

        matrix = item.listMatrix[r]

        for j in range(matrix.shape[1]):
            for i in range(matrix.shape[0]):
                if matrix[i][j] > 0:
                    sqver = np.array([[i, j], [i+1, j], [i+1, j+1], [i, j+1]])*h
                    for i in range(sqver.shape[0]):
                        sqver[i][0] += item.lb_x
                        sqver[i][1] += item.lb_y
                    polygon = patches.Polygon(sqver, linewidth=1, facecolor='silver', edgecolor='black', alpha = 0.33)
                    ax.add_patch(polygon)
        polygon = patches.Polygon(item.points, linewidth=1, edgecolor='red', fill = False)
        ax.add_patch(polygon)
        
    plt.savefig('pallet' + str(items[0].pallet_number) + '.png')
    return fig, ax

def draw_all_pallets(packing, pallet_width, pallet_leight, h):
    
    for i in range(len(packing)):
        draw_pallet(packing[i], pallet_width, pallet_leight, h)