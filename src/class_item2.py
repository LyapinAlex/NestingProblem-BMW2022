import numpy as np

from class_polygon import Polygon
from class_vector import Vector

# реализовать больше одного поворота и отражение

class Item:

    def __init__(self, id: int, polygon):
        self.id = id
        if type(polygon) == Polygon:
            self.polygon = polygon
        else:
            self.polygon = Polygon(polygon)
        self.expand_polygon = None

        # ----------  Code   -----------
        self.matrix = None
        self.list_new_shift = None
        self.list_check_order = None
        self.pixel_area = None

        # --------  Position   ---------
        self.raster_coord = None
        self.optimal_x = None
        self.optimal_y = None
        self.rotation = 0
        self.reflection = False
        self.pallet_id = None

    def __str__(self):
        return str(self.polygon)

    def clear_coordinat(self):
        self.raster_coord = None
        self.optimal_x = None
        self.optimal_y = None
        self.rotation = 0
        self.reflection = False
        self.pallet_id = None
        return None

    def get_item_on_position(self):
        return

    def set_matrix(self, h, drill_radius = 0):
        if  drill_radius != 0:
            self.expand_polygon = self.polygon.expand_polygon(drill_radius)
            surf_vector = self.polygon.minXY() - self.expand_polygon.minXY()
            self.expand_polygon.move_to_origin()
            self.polygon.move_to(surf_vector)
        else:
            self.polygon.move_to_origin()
            self.expand_polygon = self.polygon.copy()
        self.matrix = self.expand_polygon.create_rastr_approximation(h)
        return

    def get_matrix_compressed_encoding(self, num_turn, is_reflection):
        return

    def list_of_new_shift_code(self, h):
        return

    def culc_pixel_area(self, new_shift):
        return

    def check_orders_in_new_shift(self, new_shift):
        return

    def draw_polygon(self, h):
        return

if (__name__ == '__main__'):
    h = 0.2
    drill_r = 0
    # it1 = Item(1, np.array([[0.3, 0.5], [0, 1], [0.7, 1.5], [1.2, 0.8], [3, 0.8], [3, 0.4], [1.2, 0.4], [0.6, 0.8]]))
    it1 = Item(1, np.array([[1, 0], [0.3, 3], [3, 3.7], [2.1, 0]]))
    print(it1)
    it1.set_matrix(h, drill_r)
    print(it1.matrix)
    it1.polygon.draw(is_draw_raster_approximation=True,h = h)
    # p2 = Polygon([
    #     Vector(2, 2),
    #     Vector(1, 1),
    #     Vector(-4, 2),
    #     Vector(5, 13),
    #     Vector(4.00012, 4),
    #     Vector(4.00006, 4),
    #     Vector(4, 4)
    # ])
    # it2 = Item(1, p2)
    # print(it2)
