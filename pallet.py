import class_item
import numpy as np

class Pallet():

    def __init__(self, id, w, l, e):
        
        self.shape = (int(w / e), int(l / e))  
        self.id = id
        self.matrix = np.zeros(self.shape, dtype =  np.uint16)
        self.items = []




