from class_DCEL import DCEL
from class_polygon import Polygon
from class_segment import Segment
from class_vector import Vector


class Nfp_Packer:
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.polygons = []

    def pack(self, polygon: Polygon):
        polygon.sort_points()
        if len(self.polygons) == 0:
            polygon.move_to_origin()
            self.polygons.append(polygon)
            return

        pallet_border = [Segment(Vector(polygon.point(0).x-polygon.minXY().x, 0), Vector(self.width-(polygon.maxXY().x-polygon.point(0).x), 0)),
                         Segment(Vector(self.width-(polygon.maxXY().x-polygon.point(0).x), 0), Vector(self.width-(
                             polygon.maxXY().x-polygon.point(0).x), self.heigth-(polygon.maxXY().y-polygon.point(0).y))),
                         Segment(Vector(self.width-(polygon.maxXY().x-polygon.point(0).x), self.heigth-(polygon.maxXY().y-polygon.point(0).y)),
                         Vector(polygon.point(0).x-polygon.minXY().x, self.heigth-(polygon.maxXY().y-polygon.point(0).y))),
                         Segment(Vector(polygon.point(0).x-polygon.minXY().x, self.heigth-(polygon.maxXY().y-polygon.point(0).y)), Vector(polygon.point(0).x-polygon.minXY().x, 0))]
        pallet_border_dcel = DCEL(pallet_border)

        no_fit_polygon_arrangement = DCEL()

        for packed_polygon in self.polygons:
            part_of_nfp = Polygon.nfp(packed_polygon, polygon)
            no_fit_polygon_arrangement = DCEL.set_or(
                no_fit_polygon_arrangement, part_of_nfp)
        no_fit_polygon_arrangement = DCEL.set_minus(
            pallet_border_dcel, no_fit_polygon_arrangement)
        optimal_point = no_fit_polygon_arrangement.vertices.min_key_node(
            no_fit_polygon_arrangement.vertices.root).key

        polygon.move_to(polygon.minXY() +
                        optimal_point-polygon.point(0))
        polygon.points[0] = optimal_point
        self.polygons.append(polygon)
