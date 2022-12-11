if __name__ == '__main__':
    from find_position import find_position
else:
    from .find_position import find_position


def find_position_with_rotation(pallet, pallet_shape, item):
    """Ищет расположение предмета для всех поворотов и выбирает лучшый из них"""
    is_placed_item = False
    x_best = pallet_shape[0] + 1
    y_best = pallet_shape[1] + 1
    rotation = 0

    for i in range(4):
        # if i == 1 or i == 3:
            is_placed_item_with_this_rotation, x_0, y_0 = find_position(item.list_new_shift[i], item.matrix.shape[(i + 1) % 2], item.list_check_order[i], pallet, pallet_shape[0])
            if is_placed_item_with_this_rotation and ((y_0 + item.matrix.shape[i % 2] < y_best) or ((y_0 + item.matrix.shape[i % 2] == y_best) and x_0 < x_best)):
                is_placed_item = True
                x_best = x_0
                y_best = y_0 + item.matrix.shape[i % 2]
                rotation = i
    return is_placed_item, x_best, y_best - item.matrix.shape[rotation % 2], rotation
