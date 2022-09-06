import numpy as np

if __name__=='__main__':
    from fit_item_with_route import fit_item_with_route
else:
    from .fit_item_with_route import fit_item_with_route


def fit_pallets(matrix_shape, items, h):
    """Жадный алгоритм (пока не учитывает того, что предмет может не влезть в палету?)"""
    pallets = []
    pallets.append(np.zeros(matrix_shape, dtype = np.uint16))
    for item in items:
        i=0
        exit = True
        while exit and i < len(pallets):
            exit = fit_item_with_route(pallets[i], item)
            if exit and i == (len(pallets)-1):
                pallets.append(np.zeros(matrix_shape, dtype = np.uint16))
            if not exit:
                item.pallet_number = i
            i+=1
    
    # Переводим растровые координаты в векторные
    for item in items:
        item.lb_x = item.lb_x * h
        item.lb_y = item.lb_y * h
    
    # вычисление высоты 
    print("Использованная площадь:", np.count_nonzero(np.sum(pallets[len(pallets)-1], axis = 1))*h,"x", matrix_shape[1]*h)

    return pallets