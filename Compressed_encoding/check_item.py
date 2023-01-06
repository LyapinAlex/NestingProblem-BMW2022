def get_pixel(list_units: list, pixel_num: int) -> tuple[int, int]:  #Decompression
    """По номеру пикселя в строке, возвращет содержание этого пикселя и номер ячейки в которой он содержится\\
    Returns:
        pixel_value: значение пикселя по pixel_num
        unit_num: номер ячейки к которой относится pixel_num"""
    sum_units = 0
    unit_num = -1
    while (sum_units < pixel_num + 1):
        unit_num += 1
        sum_units += abs(list_units[unit_num])

    pixel_value = sum_units - pixel_num
    if list_units[unit_num] < 0:
        pixel_value *= -1

    return pixel_value, unit_num


def check_pixel(pallet_pixel: int, item_pixel: int, item_unit: int) -> tuple[bool, int]:
    """Если текущее расположение возможно (is_placed_pixel=True), возвращает то на сколько надо сдвинуться вправо (shift), 
    чтоб проверить следущий пиксель пропуская пустоты предмета
    
    Если текущее расположение невозможно (is_placed_pixel=False), возвращает то на сколько надо сдвинуться вправо (shift), 
    чтоб выйти за пределы заполненности
    
    Returns:
        is_placed_pixel, shift"""
    is_placed_pixel: bool
    shift: int
    if item_pixel < 0 or pallet_pixel < 0:
        is_placed_pixel = True
        shift = -min(item_pixel, pallet_pixel)
    else:
        is_placed_pixel = False
        shift = pallet_pixel + item_unit - item_pixel
    return is_placed_pixel, shift


def check_line(x: int, item_line: list, len_item_line: int, pallet_line: list) -> tuple[bool, int]:
    """Проверяем, можно ли строчку item_line расположить в строчке pallet_line, 
    по координате x
    
    Returns:
        is_placed_line, shift"""
    is_placed_line = True
    shift = 0
    write_read_head = 0
    while is_placed_line and write_read_head < len_item_line:
        pallet_pixel_value, pallet_unit_num = get_pixel(
            pallet_line, x + write_read_head)
        item_pixel_value, item_unit_num = get_pixel(item_line,
                                                     write_read_head)

        is_placed_line, shift = check_pixel(pallet_pixel_value,
                                            item_pixel_value,
                                            item_line[item_unit_num])
        write_read_head += shift

    return is_placed_line, shift


def check_item(pallet, item_encoding, positon, bad_line: int) -> tuple[bool, int, int]:
    """Проверяем, можно ли item_encoding расположить в pallet, по координатам positon
    
    Returns:
        is_placed_item, shift, bad_line"""

    pallet_ce = pallet.compressed_encoding
    item_ce = item_encoding.compressed_encoding
    item_hl = item_encoding.horizontal_length
    item_vl = item_encoding.vertical_length
    check_order = item_encoding.line_check_order
    x = positon.x
    y = positon.y

    is_placed_item = True
    j = 0
    #оптимизация которая нужна только для достаточно многострочных кодировок
    if (y < bad_line) and (item_vl > 40):
        is_placed_item, shift = check_line(x, item_ce[bad_line - y], item_hl,
                                           pallet_ce[bad_line])
        if not is_placed_item:
            return is_placed_item, shift, bad_line

    while (j < item_vl) and is_placed_item:
        is_placed_item, shift = check_line(x, item_ce[check_order[j]], item_hl,
                                           pallet_ce[check_order[j] + y])
        j += 1
    return is_placed_item, shift, check_order[j - 1] + y
