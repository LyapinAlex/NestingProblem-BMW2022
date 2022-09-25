if __name__ == '__main__':
    from get_pixel import get_pixel
    from check_pixel import check_pixel
else:
    from .get_pixel import get_pixel
    from .check_pixel import check_pixel


def check_line(x: int, item_line: list, item_line_length: int, pallet_line: list):
    """Проверяем, можно ли строчку item_line расположить в строчке pallet_line, 
    по координате x
    
    Returns:
        is_placed_line, shift"""
    is_placed_line = True
    shift = 0
    write_read_head = 0 #analog of the Turing machine
    while is_placed_line and write_read_head < item_line_length:
        pal_r, pal_i = get_pixel(pallet_line, x + write_read_head)
        it_r, it_i = get_pixel(item_line, write_read_head)
        is_placed_line, shift = check_pixel(pal_r, it_r, item_line[it_i])
        write_read_head += shift
    return is_placed_line, shift