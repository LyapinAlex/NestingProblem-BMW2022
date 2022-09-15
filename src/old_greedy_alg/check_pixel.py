def check_pixel(pal_pixel, item_pixel):
    """Если текущее расположение возможно (placed=True), возвращает то на сколько надо сдвинуться вправо (shift), 
    чтоб проверить следущий пиксель пропуская пустоты предмета
    
    Если текущее расположение невозможно (placed=False), возвращает то на сколько надо сдвинуться вправо (shift), 
    чтоб выйти за пределы заполненности
    
    Returns:
        placed, shift"""
    placed = None
    shift = None

    if item_pixel < 0:
        placed = True
        shift = -item_pixel
    elif pal_pixel == 0:
        placed = True
        shift = 1
    else:
        placed = False
        shift = pal_pixel
    return placed, shift