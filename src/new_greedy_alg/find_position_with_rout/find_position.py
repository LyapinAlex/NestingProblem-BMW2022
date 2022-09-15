if __name__ == '__main__':
    from check_item import check_item
else:
    from .check_item import check_item


def find_position(item, len_it: int, pallet, len_pal: int, x=0, y=0):
    """Ищет возможное расположение объекта по принципу жадного алгоритма "как можно ниже, как можно левее"
    
    Returns:
        placed: bool 
        x, y: int - растровые координаты возможного расположения"""
    shift = 0
    placed = False
    while (not placed) and (y + item.shape[0] <= pallet.shape[0]):
        while (not placed) and (x + shift + len_it <= len_pal):
            x += shift
            placed, shift = check_item(item, len_it, pallet, x, y)
            # print(x, shift, len_it, len_pal)
        if not placed:
            y += 1
            x = 0
            shift = 0
    return placed, x, y