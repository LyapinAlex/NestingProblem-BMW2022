import numpy as np


def create_pallet(pallet_shape):
    pallet = np.full(pallet_shape[1], None)
    for i in range(pallet_shape[1]):
        pallet[i] = [-pallet_shape[0]]
    return pallet