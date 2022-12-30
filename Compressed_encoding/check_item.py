def get_pixel(li: list, iter: int):  #Decompression
    """
    По номеру пикселя в строке, возвращет содержание этого пикселя и номер ячейки в которой он содержится
    Returns:
        int: значение пикселя по iter
        i: номер ячейки к которой относится iter"""
    r = 0
    i = -1
    sign = 1
    while (r < iter + 1):
        i += 1
        r += abs(li[i])
    if li[i] < 0: sign = -1
    return sign * (r - iter), i


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


def check_line(x: int, item_line: list, item_line_length: int,
               pallet_line: list):
    """Проверяем, можно ли строчку item_line расположить в строчке pallet_line, 
    по координате x
    
    Returns:
        is_placed_line, shift"""
    is_placed_line = True
    shift = 0
    write_read_head = 0  # analog of the Turing machine
    while is_placed_line and write_read_head < item_line_length:
        pal_r, pal_i = get_pixel(pallet_line, x + write_read_head)
        it_r, it_i = get_pixel(item_line, write_read_head)
        is_placed_line, shift = check_pixel(pal_r, it_r, item_line[it_i])
        write_read_head += shift
    return is_placed_line, shift


def check_item(pallet, item_enc, positon, bad_line: int):
    """Проверяем, можно ли item_enc расположить в pallet, по координатам positon
    
    Returns:
        is_placed_item, shift, bad_line"""

    item_shift_code = item_enc.compressed_encoding
    item_line_length = item_enc.horizontal_length
    check_order = item_enc.line_check_order
    pallet_shift_code = pallet.compressed_encoding
    x = positon.x
    y = positon.y

    is_placed_item = True
    j = 0
    #оптимизация которая нужна только для достаточно многострочных кодировок
    if (y < bad_line) and (item_shift_code.shape[0] > 40):
        is_placed_item, shift = check_line(x, item_shift_code[bad_line - y],
                                           item_line_length,
                                           pallet_shift_code[bad_line])
        if not is_placed_item:
            return is_placed_item, shift, bad_line

    while (j < item_shift_code.shape[0]) and is_placed_item:
        is_placed_item, shift = check_line(
            x, item_shift_code[check_order[j]], item_line_length,
            pallet_shift_code[check_order[j] + y])
        j += 1
    return is_placed_item, shift, check_order[j - 1] + y
