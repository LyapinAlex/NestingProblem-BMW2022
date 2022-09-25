if __name__ == '__main__':
    from check_item import check_item
else:
    from .check_item import check_item


def find_position(item_shift_code, item_line_length: int, check_order, pallet_shift_code, pallet_line_length: int):
    """Ищет возможное расположение объекта по принципу жадного алгоритма "как можно ниже, как можно левее"
    
    Returns:
        is_placed_item: bool 
        x, y: int - растровые координаты возможного расположения"""
    x = 0
    y = 0
    shift = 0
    is_placed_item = False
    bad_line = 0
    while (not is_placed_item) and (y + item_shift_code.shape[0] <= pallet_shift_code.shape[0]):
        while (not is_placed_item) and (x + shift + item_line_length <= pallet_line_length):
            x += shift
            is_placed_item, shift, bad_line = check_item(item_shift_code, item_line_length, check_order, pallet_shift_code, x, y, bad_line)
        if not is_placed_item:
            y += 1
            x = 0
            shift = 0
    return is_placed_item, x, y