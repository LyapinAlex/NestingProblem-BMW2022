import numpy as np

if __name__ == '__main__':
    from check_line import check_line
else:
    from .check_line import check_line


def check_item(item_shift_code,  item_line_length: int, check_order, pallet_shift_code, x: int, y: int, bad_line: int):
    """Проверяем, можно ли item_shift_code расположить в pallet_shift_code, 
    по координатам x, y
    
    Returns:
        is_placed_item, shift"""

    is_placed_item = True
    j = 0

    if (y < bad_line) and (item_shift_code.shape[0] > 25): #оптимизация которая нужна только для достаточно больших предметов
        is_placed_item, shift = check_line(x, item_shift_code[bad_line-y],  item_line_length, pallet_shift_code[bad_line])
        if not is_placed_item:
            return is_placed_item, shift, bad_line

    while (j < item_shift_code.shape[0]) and is_placed_item:
        is_placed_item, shift = check_line(x, item_shift_code[check_order[j]],  item_line_length, pallet_shift_code[check_order[j] + y])
        j += 1
    return is_placed_item, shift, check_order[j-1] + y