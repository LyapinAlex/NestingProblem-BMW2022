if __name__ == '__main__':
    from find_position import find_position
else:
    from .find_position import find_position


def find_position_with_rout(pallet, pallet_shape, item, x=0, y=0):
    """Ищет расположение предмета для всех поворотов и выбирает лучшый из них"""
    placed_item = False
    x_b = pallet_shape[0] + 1
    y_b = pallet_shape[1] + 1
    rout = 0

    for i in range(4):
        placed_item, x_0, y_0 = find_position(item.list_new_shift[i], item.matrix.shape[(i + 1) % 2], pallet, pallet_shape[0], x, y)
        if placed_item and ((y_0 + item.matrix.shape[i % 2] < y_b) or ((y_0 + item.matrix.shape[i % 2] == y_b) and x_0 < x_b)):
            placed_item = True
            x_b = x_0
            y_b = y_0 + item.matrix.shape[i % 2]
            rout = i
    return placed_item, x_b, y_b - item.matrix.shape[rout % 2], rout
