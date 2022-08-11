import copy
import math
from FitItem import fit_item


def fit_item_all_route(pallet, item):
    bonder = len(pallet)

    copyPallet = copy.deepcopy(pallet)

    exit = True
    for r in range(4):
        copyItem = copy.deepcopy(item)
        sol = fit_item(copy.deepcopy(copyPallet), copyItem)
        if sol[1] == False:
            if copyItem.lb_x + len(copyItem.matrix) <= bonder:
                item.lb_x = copyItem.lb_x
                item.lb_y = copyItem.lb_y
                pallet = sol[0]
                item.rotation = r * math.pi / 2
                exit = False
                bonder = copyItem.lb_x + len(copyItem.matrix)

        item.rotationMatrix()

    return pallet, exit


def find_lb_coordinates(items, eps):
    for item in items:
        item.lb_x = item.lb_x * eps
        item.lb_y = item.lb_y * eps

    return items


def fit_pallets(matrix, items, eps):
    pallets = []
    pallets.append(copy.deepcopy(matrix))
    for item in items:
        # print(item.matrix)
        i=0
        exit = True
        while exit and i<len(pallets):
            # print(i)
            pallets[i], exit = fit_item_all_route(pallets[i], item)
            if exit and i==(len(pallets)-1):
                pallets.append(copy.deepcopy(matrix))
            if not exit:
                item.pallet_number = i
                # print(i)
            i+=1
        # print('!!!!!!!!!!!!!!!!')
        # for pal in  pallets:
        #     for l in pal:
        #         print(l)

        # print('!!!!!!!!!!!!!!!!')

    # print_matrix(pallets)
    find_lb_coordinates(items, eps)

    return pallets