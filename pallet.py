import numpy as np

class Pallet():

    def __init__(self, id, w, l, h):
        self.shape = (int(w / h), int(l / h))  
        self.id = id
        self.matrix = np.zeros(self.shape, dtype =  np.uint16)
        self.items = []




