import class_item
import numpy as np
import math

class Pallet():

    def __init__(self, id, w, l, e):
        shape = (math.ceil(w / e), math.ceil(l / e))  

        self.id = id
        self.matrix = np.zeros(shape, dtype = 'int').tolist() 
        self.items = []




