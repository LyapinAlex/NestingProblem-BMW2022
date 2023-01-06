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


def fit_unit(pallet_line: list, item_line: list, x: int, num_item_unit: int) -> None:
    """Производит подстановку положительной ячейки предмета (num_item_unit) в отрицательную ячейку паллеты, по коодинате x"""
    pallet_pixel, num_pallet_unit = get_pixel(pallet_line, x)
    num_pixels_left = pallet_line[num_pallet_unit] - pallet_pixel
    num_pixels_right = pallet_pixel + item_line[num_item_unit]

    if 0 < num_pallet_unit and num_pallet_unit + 1 < len(pallet_line):
        if num_pixels_left == 0 and num_pixels_right == 0:
            # случай 1.1
            pallet_line[num_pallet_unit - 1] += -pallet_line.pop(num_pallet_unit)
            pallet_line[num_pallet_unit - 1] += pallet_line.pop(num_pallet_unit)

        elif num_pixels_left != 0 and num_pixels_right != 0:
            # случай 1.2
            pallet_line.insert(num_pallet_unit + 1, num_pixels_right)
            pallet_line[num_pallet_unit] = item_line[num_item_unit]
            pallet_line.insert(num_pallet_unit, num_pixels_left)

        elif num_pixels_left == 0 and num_pixels_right != 0:
            # случай 1.3
            pallet_line[num_pallet_unit] = num_pixels_right
            pallet_line[num_pallet_unit - 1] += item_line[num_item_unit]

        else:
            # случай 1.4
            pallet_line[num_pallet_unit] = num_pixels_left
            pallet_line[num_pallet_unit + 1] += item_line[num_item_unit]

    elif num_pallet_unit == 0 and len(pallet_line) != 1:
        if num_pixels_left == 0 and num_pixels_right == 0:
            # случай 2.1
            pallet_line.pop(num_pallet_unit)
            pallet_line[num_pallet_unit] += item_line[num_item_unit]

        elif num_pixels_left != 0 and num_pixels_right != 0:
            # случай 2.2 (1.2)
            pallet_line.insert(num_pallet_unit + 1, num_pixels_right)
            pallet_line[num_pallet_unit] = item_line[num_item_unit]
            pallet_line.insert(num_pallet_unit, num_pixels_left)

        elif num_pixels_left == 0 and num_pixels_right != 0:
            # случай 2.3 (4.3)
            pallet_line[num_pallet_unit] = num_pixels_right
            pallet_line.insert(num_pallet_unit, item_line[num_item_unit])

        else:
            # случай 2.4 (1.4)
            pallet_line[num_pallet_unit] = num_pixels_left
            pallet_line[num_pallet_unit + 1] += item_line[num_item_unit]

    elif num_pallet_unit == len(pallet_line) - 1 and len(pallet_line) != 1:
        if num_pixels_left == 0 and num_pixels_right == 0:
            # случай 3.1
            pallet_line.pop(num_pallet_unit)
            pallet_line[num_pallet_unit - 1] += item_line[num_item_unit]

        elif num_pixels_left != 0 and num_pixels_right != 0:
            # случай 3.2 (1.2)
            pallet_line.insert(num_pallet_unit + 1, num_pixels_right)
            pallet_line[num_pallet_unit] = item_line[num_item_unit]
            pallet_line.insert(num_pallet_unit, num_pixels_left)

        elif num_pixels_left == 0 and num_pixels_right != 0:
            # случай 3.3 (1.3)
            pallet_line[num_pallet_unit] = num_pixels_right
            pallet_line[num_pallet_unit - 1] += item_line[num_item_unit]

        else:
            # случай 3.4 (4.4)
            pallet_line[num_pallet_unit] = num_pixels_left
            pallet_line.insert(num_pallet_unit + 1, item_line[num_item_unit])

    elif len(pallet_line) == 1:
        if num_pixels_left == 0 and num_pixels_right == 0:
            # случай 4.1
            pallet_line[num_pallet_unit] *= -1

        elif num_pixels_left != 0 and num_pixels_right != 0:
            # случай 4.2 (1.2)
            pallet_line.insert(num_pallet_unit + 1, num_pixels_right)
            pallet_line[num_pallet_unit] = item_line[num_item_unit]
            pallet_line.insert(num_pallet_unit, num_pixels_left)

        elif num_pixels_left == 0 and num_pixels_right != 0:
            # случай 4.3
            pallet_line[num_pallet_unit] = num_pixels_right
            pallet_line.insert(num_pallet_unit, item_line[num_item_unit])

        else:
            # случай 4.4
            pallet_line[num_pallet_unit] = num_pixels_left
            pallet_line.insert(num_pallet_unit + 1, item_line[num_item_unit])

    else:
        raise Exception("Ошибка заполнения паллеты/логики программы")


def fit_line(pallet_line: list, item_line: list, x: int) -> None:
    """Производит подстановку строки предмета в строку паллеты начиная с x координаты строки паллеты"""
    num_first_positive_unit_of_line = 0
    if item_line[num_first_positive_unit_of_line] < 0:
        x -= item_line[num_first_positive_unit_of_line]
        num_first_positive_unit_of_line = 1

    for num_positive_unit_of_line in range(num_first_positive_unit_of_line, len(item_line), 2):
        fit_unit(pallet_line, item_line, x, num_positive_unit_of_line)
        if num_positive_unit_of_line + 2 < len(item_line):
            x += item_line[num_positive_unit_of_line] + abs(item_line[num_positive_unit_of_line + 1])


def fit_item(pallet_shift_code, item_shift_code, positon) -> None:
    """Размещает объект на паллете по координатам (x,y), без проверки на возможность размещения"""
    x = positon.x
    y = positon.y
    for i in range(item_shift_code.shape[0]):
        fit_line(pallet_shift_code[y + i], item_shift_code[i], x)
