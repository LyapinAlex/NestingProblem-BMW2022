from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np
import math
import copy


def draw_pallet(items, pallet_width, pallet_height, eps):


    fig, ax = plt.subplots()
    MAX_SIZE = 7
    if pallet_width > pallet_height:
        fig.set_figheight(MAX_SIZE * pallet_height/pallet_width)
        fig.set_figwidth(MAX_SIZE)
    else:
        fig.set_figheight(MAX_SIZE)
        fig.set_figwidth(MAX_SIZE * pallet_width/pallet_height)

   
    pallet = patches.Rectangle((0, 0), pallet_width, pallet_height, linewidth=2, facecolor='none', edgecolor='black')
    ax.add_patch(pallet)
    ax.set_xlim(-0.5, pallet_width + 0.5)
    ax.set_ylim(-0.5, pallet_height + 0.5)

    for item in items:
       
        # item.surfPoint()
        pointsCopy = copy.deepcopy(item.points)
        r = int(item.rotation*2 / math.pi)

        print(r)

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

   
        
        
        # print('?')
        
        # print(item.surfPoint())

        for point in item.points:

            
            if r == 0:
                point[0] += item.lb_x
                point[1] += item.lb_y
            if r == 1:

                point[0] += item.lb_x + eps*len(item.matrix[0])
                point[1] += item.lb_y

            if r == 2:
                point[0] += item.lb_x + eps*len(item.matrix)
                point[1] += item.lb_y + eps*len(item.matrix[0])
            if r == 3:

                point[0] += item.lb_x
                point[1] += item.lb_y + eps*len(item.matrix)

      



        # for point in item.points:
        #     point[0] += item.lb_x
        #     point[1] += item.lb_y

        # print(pointsCopy)



        polygon = patches.Polygon(item.points, linewidth=1, facecolor='silver', edgecolor='black')
        ax.add_patch(polygon)

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