from __future__ import annotations
from math import sqrt
from xml.dom import minidom
from svg.path import parse_path
from svg.path.path import Line, CubicBezier
from class_polygon import Polygon
import os


def b3(x0, y0, x1, y1, x2, y2, x3, y3, d=5):
    px = (x3 - x0) / 3
    py = (y3 - y0) / 3
    mx1 = x1 - x0 - px
    my1 = y1 - y0 - py
    mx2 = x2 - x3 + px
    my2 = y2 - y3 + py
    d1 = sqrt(mx1**2 + my1**2)
    d2 = sqrt(mx2**2 + my2**2)
    if d1 < d and d2 < d:
        return [[x3, y3]]
    else:
        x01 = (x0 + x1) / 2
        y01 = (y0 + y1) / 2
        x12 = (x1 + x2) / 2
        y12 = (y1 + y2) / 2
        x23 = (x2 + x3) / 2
        y23 = (y2 + y3) / 2
        x012 = (x01 + x12) / 2
        y012 = (y01 + y12) / 2
        x123 = (x12 + x23) / 2
        y123 = (y12 + y23) / 2
        x0123 = (x012 + x123) / 2
        y0123 = (y012 + y123) / 2
        return b3(x0, y0, x01, y01, x012, y012, x0123, y0123, d) + b3(
            x0123, y0123, x123, y123, x23, y23, x3, y3, d)


def svg_2_polygon_and_metadata(file_name):
    doc = minidom.parse(file_name)
    paths = doc.getElementsByTagName('path')
    polygons = []
    gs = doc.getElementsByTagName('g')
    gs = list(filter(lambda g: g.getElementsByTagName('metadata') != [], gs))
    initial_xml = gs[0].toxml()
    for path in paths:
        polygon = []
        path_string = parse_path(path.getAttribute('d'))
        for e in path_string:
            if isinstance(e, Line):
                polygon += [[e.start.real, -e.start.imag]]
            elif isinstance(e, CubicBezier):
                polygon += b3(e.start.real, -e.start.imag, e.control1.real,
                              -e.control1.imag, e.control2.real,
                              -e.control2.imag, e.end.real, -e.end.imag)[:-1]
        polygons.append(polygon)
    doc.unlink()
    return polygons, initial_xml


def save_pallet_as_TXT(path, polygons: list[Polygon]):
    """Создаёт файл содержащий многоугольники из массива"""
    f = open(path + '\\all_autocovers.txt', 'w')
    f.write(str(len(polygons)*2) + '\n')
    f.write(str(1000000) + " " + str(800000) + '\n')
    for polygon in polygons:
        points = polygon.points_to_list()
        s = ''
        for point in points:
            s += str(round(point[0], 4)) + ' ' 
            s += str(round(point[1], 4)) + ' ' 
        f.write(s + '\n')
        f.write(s + '\n')
    f.close()


def find_polygons(folder):
    file_names = [each for each in os.listdir(folder) if each.endswith('.svg')]
    result = []
    for file_name in file_names:
        candidates_for_polygon, initial_xml = svg_2_polygon_and_metadata(
            folder + "\\" + file_name)

        desired_polygon = None
        for coord in candidates_for_polygon:
            if len(coord):
                desired_polygon = Polygon(coord)

        poly_area = desired_polygon.area_circumscribed_rectangle()
        for coord in candidates_for_polygon:
            if len(coord) == 0: continue
            polygon = Polygon(coord)
            if polygon.area_circumscribed_rectangle() > poly_area:
                desired_polygon = polygon
                poly_area = polygon.area_circumscribed_rectangle()
        result.append([desired_polygon, initial_xml])

    # for polygon, initial_xml in result:
    #     polygon.draw()

    return [polygon for polygon, initial_xml in result]


if __name__ == '__main__':
    folder = "Compressed_encoding\\input\\autocovers"
    save_pallet_as_TXT("Compressed_encoding", find_polygons(folder))