import numpy as np
import math

if __name__ == '__main__':
    from create_pallet import create_pallet
    from placed_item.fit_item import fit_item
    from find_position_with_rotation.find_position_with_rotation import find_position_with_rotation
else:
    from .create_pallet import create_pallet
    from .placed_item.fit_item import fit_item
    from .find_position_with_rotation.find_position_with_rotation import find_position_with_rotation


def fit_pallets_with_rotation(pallet_shape, items, h):
    """Распологает предметы в заданном порядке на паллету жадным образом, выбирая лучший из сохранённых поворотов"""
    pallets = []
    pallets.append(create_pallet(pallet_shape))
    for item in items:
        x = 0
        y = 0
        rotation = 0
        pallet_number = -1
        is_placed_item = False
        while not is_placed_item and pallet_number < len(pallets) - 1:
            pallet_number += 1
            is_placed_item, x, y, rotation = find_position_with_rotation(pallets[pallet_number], pallet_shape, item)

        if not is_placed_item:
            pallets.append(create_pallet(pallet_shape))
            pallet_number += 1
            is_placed_item, x, y, rotation = find_position_with_rotation(pallets[pallet_number], pallet_shape, item)

        if not is_placed_item:
            print("Предмет не влазит в паллету")
        else:
            item.pallet_number = pallet_number
            item.raster_coord = (x, y)
            item.lb_x = y * h
            item.lb_y = x * h
            item.rotation = rotation * math.pi / 2
            fit_item(pallets[pallet_number], item.list_new_shift[rotation], x, y)
    return pallets