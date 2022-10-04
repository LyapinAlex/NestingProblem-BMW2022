if __name__ == '__main__':
    from get_pixel import get_pixel
else:
    from .get_pixel import get_pixel
#!!! поменять на путь до соседнего модуля и удалить лишний get_pixel


def fit_unit(pallet: list, item: list, x_0: int, i_it:int):
    """Производит подстановку положительной ячейки предмета (i_it) в отрицательную ячейку паллеты, по коодинате x_0"""
    p_p, i_p = get_pixel(pallet, x_0)
    left_r = pallet[i_p] - p_p
    right_r = p_p + item[i_it]

    if 0 < i_p and i_p + 1 < len(pallet):
        if left_r == 0 and right_r == 0:
            # случай 1.1
            pallet[i_p - 1] += -pallet.pop(i_p)
            pallet[i_p - 1] += pallet.pop(i_p)

        elif left_r != 0 and right_r != 0:
            # случай 1.2
            pallet.insert(i_p + 1, right_r)
            pallet[i_p] = item[i_it]
            pallet.insert(i_p, left_r)

        elif left_r == 0 and right_r != 0:
            # случай 1.3
            pallet[i_p] = right_r
            pallet[i_p - 1] += item[i_it]

        else:
            # случай 1.4
            pallet[i_p] = left_r
            pallet[i_p + 1] += item[i_it]

    elif i_p == 0 and len(pallet) != 1:
        if left_r == 0 and right_r == 0:
            # случай 2.1
            pallet.pop(i_p)
            pallet[i_p] += item[i_it]

        elif left_r != 0 and right_r != 0:
            # случай 2.2 (1.2)
            pallet.insert(i_p + 1, right_r)
            pallet[i_p] = item[i_it]
            pallet.insert(i_p, left_r)

        elif left_r == 0 and right_r != 0:
            # случай 2.3 (4.3)
            pallet[i_p] = right_r
            pallet.insert(i_p, item[i_it])

        else:
            # случай 2.4 (1.4)
            pallet[i_p] = left_r
            pallet[i_p + 1] += item[i_it]

    elif i_p == len(pallet) - 1 and len(pallet) != 1:
        if left_r == 0 and right_r == 0:
            # случай 3.1
            pallet.pop(i_p)
            pallet[i_p - 1] += item[i_it]

        elif left_r != 0 and right_r != 0:
            # случай 3.2 (1.2)
            pallet.insert(i_p + 1, right_r)
            pallet[i_p] = item[i_it]
            pallet.insert(i_p, left_r)

        elif left_r == 0 and right_r != 0:
            # случай 3.3 (1.3)
            pallet[i_p] = right_r
            pallet[i_p - 1] += item[i_it]

        else:
            # случай 3.4 (4.4)
            pallet[i_p] = left_r
            pallet.insert(i_p + 1, item[i_it])

    elif len(pallet) == 1:
        if left_r == 0 and right_r == 0:
            # случай 4.1
            pallet[i_p] *= -1

        elif left_r != 0 and right_r != 0:
            # случай 4.2 (1.2)
            pallet.insert(i_p + 1, right_r)
            pallet[i_p] = item[i_it]
            pallet.insert(i_p, left_r)

        elif left_r == 0 and right_r != 0:
            # случай 4.3
            pallet[i_p] = right_r
            pallet.insert(i_p, item[i_it])

        else:
            # случай 4.4
            pallet[i_p] = left_r
            pallet.insert(i_p + 1, item[i_it])

    else:
        # print("Ошибка заполнения паллеты/логики программы fit_unit")
        raise Exception("Ошибка заполнения паллеты/логики программы")
        #!!! хз как работает (raise Exception), поправить если что