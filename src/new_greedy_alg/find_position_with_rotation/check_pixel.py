def check_pixel(pal_pixel: int, item_pixel: int, item_unit=0):
    """Если текущее расположение возможно (is_placed_pixel=True), возвращает то на сколько надо сдвинуться вправо (shift), 
    чтоб проверить следущий пиксель пропуская пустоты предмета
    
    Если текущее расположение невозможно (is_placed_pixel=False), возвращает то на сколько надо сдвинуться вправо (shift), 
    чтоб выйти за пределы заполненности
    
    Returns:
        is_placed_pixel, shift"""
    is_placed_pixel = None
    shift = None
    if item_pixel < 0 or pal_pixel < 0:
        is_placed_pixel = True
        shift = -min(item_pixel, pal_pixel)
    else:
        is_placed_pixel = False
        shift = pal_pixel + item_unit - item_pixel
    return is_placed_pixel, shift