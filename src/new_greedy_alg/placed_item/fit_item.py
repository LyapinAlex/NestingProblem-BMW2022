import numpy as np

if __name__ == '__main__':
    from fit_line import fit_line
else:
    from .fit_line import fit_line


def fit_item(pallet_shift_code, item_shift_code, x: int, y: int):
    """Размещает объект на паллете по координатам (x,y), без проверки на возможность размещения"""
    for i in range(item_shift_code.shape[0]):
        fit_line(pallet_shift_code[y + i], item_shift_code[i], x)
