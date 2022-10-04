class Pallet():

    def __init__(self, width, height, h):
        """h - grid step length"""
        self.width = width
        self.height = height
        self.h = h
        self.shape = (int(width / h), int(height / h))

        # Зачем то что ниже?

        # self.id = id
        # self.matrix = np.zeros(self.shape, dtype =  np.uint16)
        # self.items = []




