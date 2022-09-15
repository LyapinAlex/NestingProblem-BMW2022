import numpy as np
import math

if __name__ == '__main__':
    from create_pallet import create_pallet
    from placed_item.fit_item import fit_item
    from find_position_with_rout.find_position_with_rout import find_position_with_rout
else:
    from .create_pallet import create_pallet
    from .placed_item.fit_item import fit_item
    from .find_position_with_rout.find_position_with_rout import find_position_with_rout


def fit_pallets_with_rout(pallet_shape, items, h):
    """Распологает предметы в заданном порядке на паллету жадным образом, выбирая лучший из сохранённых поворотов"""
    pallets = []
    pallets.append(create_pallet(pallet_shape))
    for item in items:
        x = 0
        y = 0
        rout = 0
        i = -1
        placed_item = False
        while not placed_item and i < len(pallets) - 1:
            i += 1
            placed_item, x, y, rout = find_position_with_rout(pallets[i], pallet_shape, item)

        if not placed_item:
            pallets.append(create_pallet(pallet_shape))
            i += 1
            placed_item, x, y, rout = find_position_with_rout(pallets[i], pallet_shape, item)

        if not placed_item:
            print("Предмет не влазит в паллету")
        else:
            item.pallet_number = i
            item.raster_coord = (x, y)
            item.lb_x = y * h
            item.lb_y = x * h
            item.rotation = rout * math.pi / 2
            fit_item(pallets[i], item.list_new_shift[rout], x, y)
    return pallets