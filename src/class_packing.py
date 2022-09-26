class Packing():

    def __init__(self, width, height, h, drill_radius):
        """h - grid step length"""
        self.h = h
        self.pallet_width = width
        self.pallet_height = height
        self.drill_radius = drill_radius
        self.pallet_shape = (int(width / h), int(height / h)) #округление вниз




