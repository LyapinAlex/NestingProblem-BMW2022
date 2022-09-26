class Packing():

    def __init__(self, width, height, h, drill_radius):
        """h - grid step length"""
        self.h = h
        self.pallet_width = width
        self.pallet_height = height
        self.drill_radius = drill_radius
        self.pallet_shape = (int(height / h), int(width / h))  #округление вниз

        self.num_packing_items = 0
        self.target_width = 0
        self.target_height = 0
        self.time_convert_data = 0
        self.time_packing = 0

    def print_stats(self):
        print("\nШаг сетки:", self.h)
        print("Использованная площадь:", self.target_height, "x",
              self.target_width)
        print("Время растрирования предметов:", self.time_convert_data)
        print("Время работы жадного алгоритма:", self.time_packing, '\n')

    def get_annotation(self):
        annotation = "S = " + str(self.target_height) + " x " + str(
            self.target_width) + ";  time = " + str(
                self.time_packing) + ";  Num_item = " + str(
                    self.num_packing_items) + ";  eps = " + str(self.h)
        return annotation
