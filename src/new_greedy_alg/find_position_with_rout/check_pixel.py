def check_pixel(pal_pixel: int, item_pixel: int, max_item_pixel=0):
    """Если текущее расположение возможно (placed=True), возвращает то на сколько надо сдвинуться вправо (shift), 
    чтоб проверить следущий пиксель пропуская пустоты предмета
    
    Если текущее расположение невозможно (placed=False), возвращает то на сколько надо сдвинуться вправо (shift), 
    чтоб выйти за пределы заполненности
    
    Returns:
        placed, shift"""
    placed = None
    shift = None
    if item_pixel < 0 or pal_pixel < 0:
        placed = True
        shift = -min(item_pixel, pal_pixel)
    else:
        placed = False
        shift = pal_pixel + max_item_pixel - item_pixel
    return placed, shift