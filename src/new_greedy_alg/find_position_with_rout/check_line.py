if __name__ == '__main__':
    from get_pixel import get_pixel
    from check_pixel import check_pixel
else:
    from .get_pixel import get_pixel
    from .check_pixel import check_pixel


def check_line(abs_uk: int, item: list, len_it: int, pallet: list):
    """Проверяем, можно ли строчку item расположить в строчке pallet, 
    по координате abs_uk
    
    Returns:
        placed_line, shift"""
    placed_line = True
    shift = 0
    otn_uk = 0
    while placed_line and otn_uk < len_it:
        pal_r, pal_i = get_pixel(pallet, abs_uk + otn_uk)
        it_r, it_i = get_pixel(item, otn_uk)
        placed_line, shift = check_pixel(pal_r, it_r, item[it_i])
        otn_uk += shift
    return placed_line, shift