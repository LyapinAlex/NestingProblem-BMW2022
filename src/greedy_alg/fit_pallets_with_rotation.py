import math

if __name__ == '__main__':
    from class_pallets import Pallets
    from placed_item.fit_item import fit_item
    from find_position_with_rotation.find_position_with_rotation import find_position_with_rotation
else:
    from .class_pallets import Pallets
    from .placed_item.fit_item import fit_item
    from .find_position_with_rotation.find_position_with_rotation import find_position_with_rotation


def fit_pallets_with_rotation(pallet_shape, items, h):
    """Распологает предметы в заданном порядке на паллету жадным образом, выбирая лучший из сохранённых поворотов"""
    pallets = Pallets(pallet_shape)
    pallets.add_pallet()
    for item in items:
        x = 0
        y = 0
        rotation = 0
        pallet_id = -1
        is_placed_item = False
        while not is_placed_item and pallet_id < len(pallets.pallets) - 1:
            pallet_id += 1
            is_placed_item, x, y, rotation = find_position_with_rotation(pallets.pallets[pallet_id], pallet_shape, item)

        if not is_placed_item:
            pallets.add_pallet()
            pallet_id += 1
            is_placed_item, x, y, rotation = find_position_with_rotation(pallets.pallets[pallet_id], pallet_shape, item)

        if not is_placed_item:
            print("Предмет не влазит в паллету")
            print(item.points)
        else:
            item.pallet_id = pallet_id
            item.raster_coord = (x, y)
            item.optimal_x = y * h
            item.optimal_y = x * h
            item.rotation = rotation
            fit_item(pallets.pallets[pallet_id], item.list_new_shift[rotation], x, y)
    return pallets.pallets