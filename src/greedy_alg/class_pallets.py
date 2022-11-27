from math import ceil, floor

import numpy as np


class Pallets():

    def __init__(self, pallet_shape):
        """h - grid step length"""
        self.shape = pallet_shape
        self.pallets = []
        # ----------  Segments packing   -----------
        self.grid_step = None
        self.pallet_lines = []

    def add_pallet(self):
        pallet_shift_code = np.full(self.shape[1], None)
        for i in range(self.shape[1]):
            pallet_shift_code[i] = [-self.shape[0]]
        self.pallets.append(pallet_shift_code)
        return

    def add_pallet_lines(self):
        for _ in range(ceil(self.shape[1]/self.grid_step)):
            self.pallet_lines.append([[0, 0], [self.shape[0], self.shape[0]]])
        # self.pallet_lines.append(pallet)
        return

