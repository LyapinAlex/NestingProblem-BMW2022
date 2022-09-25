import numpy as np


def create_pallet(pallet_shape):
    pallet_shift_code = np.full(pallet_shape[1], None)
    for i in range(pallet_shape[1]):
        pallet_shift_code[i] = [-pallet_shape[0]]
    return pallet_shift_code