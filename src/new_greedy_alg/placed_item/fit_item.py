import numpy as np

if __name__ == '__main__':
    from fit_line import fit_line
else:
    from .fit_line import fit_line


def fit_item(pallet, item, x: int, y: int):
    """Размещает объект на паллете по координатам (x,y), без проверки на возможность размещения"""
    for i in range(item.shape[0]):
        fit_line(pallet[y + i], item[i], x)
