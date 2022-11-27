from class_arrangement import DCEL
from class_polygon import Polygon
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

        pallet_border = [(Vector(polygon.point(0).x-polygon.minXY().x, 0), Vector(self.width-(polygon.maxXY().x-polygon.point(0).x), 0)),
                         (Vector(self.width-(polygon.maxXY().x-polygon.point(0).x), 0), Vector(self.width-(
                             polygon.maxXY().x-polygon.point(0).x), self.heigth-(polygon.maxXY().y-polygon.point(0).y))),
                         (Vector(self.width-(polygon.maxXY().x-polygon.point(0).x), self.heigth-(polygon.maxXY().y-polygon.point(0).y)),
                         Vector(polygon.point(0).x-polygon.minXY().x, self.heigth-(polygon.maxXY().y-polygon.point(0).y))),
                         (Vector(polygon.point(0).x-polygon.minXY().x, self.heigth-(polygon.maxXY().y-polygon.point(0).y)), Vector(polygon.point(0).x-polygon.minXY().x, 0))]
        pallet_border_dcel = DCEL()

        for border in pallet_border:
            pallet_border_dcel.add_edge(border)
        pallet_border_dcel.init_faces()

        no_fit_polygon_arrangement = DCEL()
        no_fit_polygon_arrangement.init_faces()

        for packed_polygon in self.polygons:
            part_of_nfp = Polygon.nfp(packed_polygon, polygon)
            no_fit_polygon_arrangement = DCEL.logical_or(
                no_fit_polygon_arrangement, part_of_nfp)

        no_fit_polygon_arrangement = DCEL.logical_minus(
            pallet_border_dcel, no_fit_polygon_arrangement)

        optimal_point = Vector(100000, 10000)

        for point in no_fit_polygon_arrangement.vertices.keys():
            if (point < optimal_point):
                optimal_point = point
        polygon.move_to(polygon.minXY() +
                        optimal_point-polygon.point(0))
        self.polygons.append(polygon)
