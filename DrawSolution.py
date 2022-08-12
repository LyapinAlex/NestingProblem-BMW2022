from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np
import math
import copy


def draw_pallet(items, pallet_width, pallet_height, eps):


    fig, ax = plt.subplots()
    fig.set_figheight(7)
    fig.set_figwidth(7)
   
    pallet = patches.Rectangle((0, 0), pallet_width, pallet_height, linewidth=2, facecolor='none', edgecolor='black')
    ax.add_patch(pallet)
    ax.set_xlim(-1, pallet_width + 1)
    ax.set_ylim(-1, pallet_height + 1)

    for item in items:
       
        # item.surfPoint()
        pointsCopy = copy.deepcopy(item.points)

        print(item.rotation)

        for point in pointsCopy:
            point0_copy = point[0]
            point1_copy = point[1]
            point[0] = math.cos(item.rotation)*point0_copy - math.sin(item.rotation)*point1_copy
            point[1] =  math.sin(item.rotation)*point0_copy + math.cos(item.rotation)*point1_copy
        
        # item.surfPoint()
        # pointsCopy

        minX = sorted(pointsCopy, key=lambda point: point[0])[0][0]
        minY = sorted(pointsCopy, key=lambda point: point[1])[0][1]

        # print(minX)
        for point in pointsCopy:
            point[0] = point[0] - minX
            point[1] = point[1] - minY

        for point in pointsCopy:
            point[0] += item.lb_x
            point[1] += item.lb_y

        polygon = patches.Polygon(pointsCopy, linewidth=1, facecolor='silver', edgecolor='black')
        ax.add_patch(polygon)

        r = int(item.rotation*2 / math.pi)
        # matrix =  np.rot90(item.matrix, r)
        matrix =  item.listMatrix[r]
        # print(np.shape(matrix))
        # print( matrix)
        for i in range(np.shape(matrix)[0]):
            for j in range(np.shape(matrix)[1]):
                
                if matrix[i,j] > 0:
                    plt.scatter([item.lb_x + eps*(i + 1/2)],[item.lb_y +eps*(j + 1/2)], c = 'r' )

   

    ax.minorticks_on()
    ax.grid(which='minor')
    plt.grid()
    plt.show()
    plt.savefig('pallet' + str(items[0].pallet_number) + '.png')
    return fig, ax

def draw_all_pallets(packing, pallet_width, pallet_leight, eps):
    
    for i in range(len(packing)):
    
        draw_pallet(packing[i], pallet_width, pallet_leight,eps)