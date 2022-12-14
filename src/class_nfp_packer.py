import math
from class_DCEL import DCEL
from class_polygon import Polygon
from class_segment import Segment
from class_vector import Vector


class Nfp_Packer:
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.polygons = []
        self.max_y = 0
        self.max_x = 0

    def pack(self, polygon: Polygon, with_rotation=False):
        optimal_optimal_point = None
        optimal_optimal_upper_point = None
        optimal_rotation = 0
        rotations = [0, 1] if with_rotation else [0]
        for rotation in rotations:
            if (rotation != 0):
                polygon.rotate(math.pi)
                polygon.expanded_polygon.rotate(math.pi)

            polygon.expanded_polygon.sort_points()
            polygon.sort_points()

            move = polygon.minXY() - polygon.expanded_polygon.minXY()
            if len(self.polygons) == 0:
                polygon.expanded_polygon.move_to_origin()
                polygon.move_to(polygon.expanded_polygon.minXY()+move)
                self.polygons.append(polygon)
                return
            pallet_border = [Segment(Vector(polygon.expanded_polygon.point(0).x-polygon.expanded_polygon.minXY().x, 0), Vector(self.width-(polygon.expanded_polygon.maxXY().x-polygon.expanded_polygon.point(0).x), 0)),
                             Segment(Vector(self.width-(polygon.expanded_polygon.maxXY().x-polygon.expanded_polygon.point(0).x), 0), Vector(self.width-(
                                 polygon.expanded_polygon.maxXY().x-polygon.expanded_polygon.point(0).x), self.heigth-(polygon.expanded_polygon.maxXY().y-polygon.expanded_polygon.point(0).y))),
                             Segment(Vector(self.width-(polygon.expanded_polygon.maxXY().x-polygon.expanded_polygon.point(0).x), self.heigth-(polygon.expanded_polygon.maxXY().y-polygon.expanded_polygon.point(0).y)),
                                     Vector(polygon.expanded_polygon.point(0).x-polygon.expanded_polygon.minXY().x, self.heigth-(polygon.expanded_polygon.maxXY().y-polygon.expanded_polygon.point(0).y))),
                             Segment(Vector(polygon.expanded_polygon.point(0).x-polygon.expanded_polygon.minXY().x, self.heigth-(polygon.expanded_polygon.maxXY().y-polygon.expanded_polygon.point(0).y)), Vector(polygon.expanded_polygon.point(0).x-polygon.expanded_polygon.minXY().x, 0))]
            pallet_border_dcel = DCEL(pallet_border)

            no_fit_polygon_arrangement = DCEL(pallet_border)

            for packed_polygon in self.polygons:
                part_of_nfp = Polygon.nfp(
                    packed_polygon, polygon.expanded_polygon)
                no_fit_polygon_arrangement = DCEL.set_minus(
                    no_fit_polygon_arrangement, part_of_nfp)
            # no_fit_polygon_arrangement = DCEL.set_minus(
            #     pallet_border_dcel, no_fit_polygon_arrangement)
            optimal_point = no_fit_polygon_arrangement.vertices.min_key_node(
                no_fit_polygon_arrangement.vertices.root).key
            if (optimal_optimal_point is None or optimal_point+polygon.expanded_polygon.maxXY()-polygon.expanded_polygon.point(0) < optimal_optimal_upper_point):
                optimal_optimal_point = optimal_point
                optimal_optimal_upper_point = optimal_point + \
                    polygon.expanded_polygon.maxXY()-polygon.expanded_polygon.point(0)
                optimal_rotation = rotation
        if (optimal_rotation == 0 and with_rotation):
            polygon.rotate(math.pi)
            polygon.expanded_polygon.rotate(math.pi)
            polygon.sort_points()
            polygon.expanded_polygon.sort_points()
        polygon.expanded_polygon.move_to(polygon.expanded_polygon.minXY() +
                                         optimal_optimal_point-polygon.expanded_polygon.point(0))
        polygon.move_to(polygon.expanded_polygon.minXY()+move)
        self.max_x = max(polygon.maxXY().x, self.max_x)
        self.max_y = max(polygon.maxXY().y, self.max_y)
        self.polygons.append(polygon)
