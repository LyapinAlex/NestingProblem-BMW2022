if __name__=='__main__':
    from check_pixel import check_pixel
else:
    from .check_pixel import check_pixel


def check_item(pallet, item_matrix):
    """Ищет место где можно расположить объект
    
    Returns:
        placed_item, lb_x, lb_y"""
    lb_x = -1
    lb_y = -1
    placed_item = False
    i = 0
    while (i < pallet.shape[0] - item_matrix.shape[0] + 1) and not placed_item:
        j = 0
        while (j < pallet.shape[1] - item_matrix.shape[1] + 1) and not placed_item:
            p = 0
            placed_pixel = True
            while (p < item_matrix.shape[0]) and placed_pixel:
                k = 0
                while (k < item_matrix.shape[1]) and placed_pixel:
                    placed_pixel, shift = check_pixel(pallet[i + p][j + k], item_matrix[p][k])
                    k += shift
                p += 1
            if placed_pixel:
                placed_item = True
                lb_x = i
                lb_y = j
            j += 1
        i += 1
    return placed_item, lb_x, lb_y