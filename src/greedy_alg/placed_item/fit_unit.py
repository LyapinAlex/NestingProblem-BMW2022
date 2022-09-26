if __name__ == '__main__':
    from get_pixel import get_pixel
else:
    from .get_pixel import get_pixel
#!!! поменять на путь до соседнего модуля и удалить лишний get_pixel


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
        # print("Ошибка заполнения паллеты/логики программы fit_unit")
        raise Exception("Ошибка заполнения паллеты/логики программы")
        #!!! хз как работает (raise Exception), поправить если что