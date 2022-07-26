import numpy as np


class Pallets():

    def __init__(self, pallet_shape):
        """h - grid step length"""
        self.shape = pallet_shape
        self.pallets = []


    def add_pallet(self):
        pallet_shift_code = np.full(self.shape[1], None)
        for i in range(self.shape[1]):
            pallet_shift_code[i] = [-self.shape[0]]
        self.pallets.append(pallet_shift_code)
        return
