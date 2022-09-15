import numpy as np

if __name__ == '__main__':
    from check_line import check_line
else:
    from .check_line import check_line


def check_item(item, len_it: int, pallet, x: int, y: int):
    """Проверяем, можно ли item расположить в pallet, 
    по координатам x, y
    
    Returns:
        placed, shift"""

    placed = True
    j = 0
    while (j < item.shape[0]) and placed:
        placed, shift = check_line(x, item[j], len_it, pallet[j + y])
        j += 1
    return placed, shift