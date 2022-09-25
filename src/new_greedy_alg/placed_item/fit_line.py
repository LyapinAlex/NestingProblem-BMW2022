if __name__ == '__main__':
    from fit_unit import fit_unit
else:
    from .fit_unit import fit_unit


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
