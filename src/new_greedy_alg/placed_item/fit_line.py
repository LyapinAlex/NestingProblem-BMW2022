if __name__ == '__main__':
    from fit_unit import fit_unit
else:
    from .fit_unit import fit_unit


def fit_line(pallet: list, item: list, x_0: int):
    """Производит подстановку строки предмета в строку паллеты начиная с x_0 координаты строки паллеты"""
    i_it = 0
    if item[i_it] < 0:
        x_0 -= item[i_it]
        i_it = 1

    for i in range(i_it, len(item), 2):
        fit_unit(pallet, item, x_0, i)
        if i + 2 < len(item):
            x_0 += item[i] + abs(item[i + 1])
