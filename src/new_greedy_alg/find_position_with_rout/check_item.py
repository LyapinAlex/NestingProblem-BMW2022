import numpy as np

if __name__ == '__main__':
    from check_line import check_line
else:
    from .check_line import check_line


def check_item(item, len_it: int, check_order, pallet, x: int, y: int, bad_line: int):
    """Проверяем, можно ли item расположить в pallet, 
    по координатам x, y
    
    Returns:
        placed, shift"""

    placed = True
    j = 0

    if (y < bad_line):
        placed, shift = check_line(x, item[bad_line-y], len_it, pallet[bad_line])
        if not placed:
            return placed, shift, bad_line

    while (j < item.shape[0]) and placed:
        placed, shift = check_line(x, item[check_order[j]], len_it, pallet[check_order[j] + y])
        j += 1
    return placed, shift, check_order[j-1] + y