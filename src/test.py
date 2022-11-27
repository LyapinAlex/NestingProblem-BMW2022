
from queue import Queue
from cmath import pi
from copy import deepcopy
from math import atan2
import time
from matplotlib import pyplot as plt
from numpy import sign
from class_arrangement import DCEL
from class_direction import is_convex, isBetween
from class_nfp_packer import Nfp_Packer
from class_polygon import Polygon
from class_vector import Vector
from shapely.geometry import LineString, Point

from putting_data.dxf2polygons import dxf2polygons


def draw_segments_sequence(segments):
    for segment in segments:
        plt.arrow(segment[0].x, segment[0].y, segment[1].x-segment[0].x, segment[1].y-segment[0].y,
                  shape='full', lw=0.5, length_includes_head=True, head_width=.05)
    plt.show()


if __name__ == '__main__':

    poly1 = Polygon([Vector(0.0, 0.0), Vector(1.0, -3.0),
                     Vector(2.0, 0.0), Vector(1.0, 3.0)])
    poly1.sort_points()
    poly2 = Polygon([Vector(0.0, 0.0), Vector(1.0, 0.0),
                     Vector(1.0, 1.0), Vector(0.0, 1.0)])
    poly2.sort_points()
    poly3 = Polygon([Vector(0.0, 0.0), Vector(2.0, 0.0), Vector(1.0, 4.0)])
    poly3.sort_points()
    # polygons = dxf2polygons(
    #     r'C:\Users\1\Desktop\NestingProblem-BMW2022\src\input\NEST001-108.DXF')
    polygons = []
    for i in range(1):
        polygons.append(deepcopy(poly2))
        polygons.append(deepcopy(poly1))
        polygons.append(deepcopy(poly2))
        polygons.append(deepcopy(poly3))
        polygons.append(deepcopy(poly2))
        polygons.append(deepcopy(poly2))
        polygons.append(deepcopy(poly1))
        polygons.append(deepcopy(poly2))
        polygons.append(deepcopy(poly3))
        polygons.append(deepcopy(poly2))
        polygons.append(deepcopy(poly1))
        polygons.append(deepcopy(poly1))
        polygons.append(deepcopy(poly2))
        polygons.append(deepcopy(poly3))
        polygons.append(deepcopy(poly2))
        polygons.append(deepcopy(poly1))
        polygons.append(deepcopy(poly2))
    # polygons = polygons[:5]
    # for polygon in polygons:
    #     polygon.sort_points()
    start_time = time.time()

    pallet = Nfp_Packer(1000, 2000)
    for polygon in polygons:
        pallet.pack(polygon)

    print(time.time() - start_time)
    aaa = []
    for polygon in pallet.polygons:
        for i in range(len(polygon.points)):
            aaa.append([polygon.point(i), polygon.next(i)])

    draw_segments_sequence(aaa)
