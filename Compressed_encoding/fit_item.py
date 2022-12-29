def get_pixel(li: list, iter: int):
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


def fit_unit(pallet_line: list, item_line: list, x: int, number_item_unit:int):
    """Производит подстановку положительной ячейки предмета (number_item_unit) в отрицательную ячейку паллеты, по коодинате x"""
    pallet_pixel, number_pallet_unit = get_pixel(pallet_line, x)
    number_pixels_left = pallet_line[number_pallet_unit] - pallet_pixel
    number_pixels_right = pallet_pixel + item_line[number_item_unit]

    if 0 < number_pallet_unit and number_pallet_unit + 1 < len(pallet_line):
        if number_pixels_left == 0 and number_pixels_right == 0:
            # случай 1.1
            pallet_line[number_pallet_unit - 1] += -pallet_line.pop(number_pallet_unit)
            pallet_line[number_pallet_unit - 1] += pallet_line.pop(number_pallet_unit)

        elif number_pixels_left != 0 and number_pixels_right != 0:
            # случай 1.2
            pallet_line.insert(number_pallet_unit + 1, number_pixels_right)
            pallet_line[number_pallet_unit] = item_line[number_item_unit]
            pallet_line.insert(number_pallet_unit, number_pixels_left)

        elif number_pixels_left == 0 and number_pixels_right != 0:
            # случай 1.3
            pallet_line[number_pallet_unit] = number_pixels_right
            pallet_line[number_pallet_unit - 1] += item_line[number_item_unit]

        else:
            # случай 1.4
            pallet_line[number_pallet_unit] = number_pixels_left
            pallet_line[number_pallet_unit + 1] += item_line[number_item_unit]

    elif number_pallet_unit == 0 and len(pallet_line) != 1:
        if number_pixels_left == 0 and number_pixels_right == 0:
            # случай 2.1
            pallet_line.pop(number_pallet_unit)
            pallet_line[number_pallet_unit] += item_line[number_item_unit]

        elif number_pixels_left != 0 and number_pixels_right != 0:
            # случай 2.2 (1.2)
            pallet_line.insert(number_pallet_unit + 1, number_pixels_right)
            pallet_line[number_pallet_unit] = item_line[number_item_unit]
            pallet_line.insert(number_pallet_unit, number_pixels_left)

        elif number_pixels_left == 0 and number_pixels_right != 0:
            # случай 2.3 (4.3)
            pallet_line[number_pallet_unit] = number_pixels_right
            pallet_line.insert(number_pallet_unit, item_line[number_item_unit])

        else:
            # случай 2.4 (1.4)
            pallet_line[number_pallet_unit] = number_pixels_left
            pallet_line[number_pallet_unit + 1] += item_line[number_item_unit]

    elif number_pallet_unit == len(pallet_line) - 1 and len(pallet_line) != 1:
        if number_pixels_left == 0 and number_pixels_right == 0:
            # случай 3.1
            pallet_line.pop(number_pallet_unit)
            pallet_line[number_pallet_unit - 1] += item_line[number_item_unit]

        elif number_pixels_left != 0 and number_pixels_right != 0:
            # случай 3.2 (1.2)
            pallet_line.insert(number_pallet_unit + 1, number_pixels_right)
            pallet_line[number_pallet_unit] = item_line[number_item_unit]
            pallet_line.insert(number_pallet_unit, number_pixels_left)

        elif number_pixels_left == 0 and number_pixels_right != 0:
            # случай 3.3 (1.3)
            pallet_line[number_pallet_unit] = number_pixels_right
            pallet_line[number_pallet_unit - 1] += item_line[number_item_unit]

        else:
            # случай 3.4 (4.4)
            pallet_line[number_pallet_unit] = number_pixels_left
            pallet_line.insert(number_pallet_unit + 1, item_line[number_item_unit])

    elif len(pallet_line) == 1:
        if number_pixels_left == 0 and number_pixels_right == 0:
            # случай 4.1
            pallet_line[number_pallet_unit] *= -1

        elif number_pixels_left != 0 and number_pixels_right != 0:
            # случай 4.2 (1.2)
            pallet_line.insert(number_pallet_unit + 1, number_pixels_right)
            pallet_line[number_pallet_unit] = item_line[number_item_unit]
            pallet_line.insert(number_pallet_unit, number_pixels_left)

        elif number_pixels_left == 0 and number_pixels_right != 0:
            # случай 4.3
            pallet_line[number_pallet_unit] = number_pixels_right
            pallet_line.insert(number_pallet_unit, item_line[number_item_unit])

        else:
            # случай 4.4
            pallet_line[number_pallet_unit] = number_pixels_left
            pallet_line.insert(number_pallet_unit + 1, item_line[number_item_unit])

    else:
        raise Exception("Ошибка заполнения паллеты/логики программы")


def fit_line(pallet_line: list, item_line: list, x: int):
    """Производит подстановку строки предмета в строку паллеты начиная с x координаты строки паллеты"""
    number_first_positive_unit_of_line = 0
    if item_line[number_first_positive_unit_of_line] < 0:
        x -= item_line[number_first_positive_unit_of_line]
        number_first_positive_unit_of_line = 1

    for number_positive_unit_of_line in range(number_first_positive_unit_of_line, len(item_line), 2):
        fit_unit(pallet_line, item_line, x, number_positive_unit_of_line)
        if number_positive_unit_of_line + 2 < len(item_line):
            x += item_line[number_positive_unit_of_line] + abs(item_line[number_positive_unit_of_line + 1])


def fit_item(pallet_shift_code, item_shift_code, positon):
    """Размещает объект на паллете по координатам (x,y), без проверки на возможность размещения"""
    x = positon.x
    y = positon.y
    for i in range(item_shift_code.shape[0]):
        fit_line(pallet_shift_code[y + i], item_shift_code[i], x)
