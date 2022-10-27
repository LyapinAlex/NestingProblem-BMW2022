
from queue import Queue
from cmath import pi
from copy import deepcopy
from math import atan2
from matplotlib import pyplot as plt
from numpy import sign
from class_DCEL import DCEL
from class_arrangement import Arrangement
from class_polygon import Polygon
from class_vector import Vector
from shapely.geometry import LineString


def is_convex(p1: Vector, p2: Vector, p3: Vector):
    return psevdoProd(p2-p1, p3-p2) > 0


def psevdoProd(p1: Vector, p2: Vector):
    return p1.x*p2.y-p1.y*p2.x


def counterclockwise_angle(p1: Vector, p2: Vector):
    dot = p1.x*p2.x + p1.y*p2.y
    det = p1.x*p2.y-p1.y*p2.x
    angle = atan2(det, dot)
    return angle if angle >= 0 else angle+2*pi


def is_collinear(vec1: Vector, vec2: Vector):
    quadrant_1 = (1 if vec1.y >= 0 else 4) if vec1.x >= 0 else (
        2 if vec1.y >= 0 else 3)
    quadrant_2 = (1 if vec2.y >= 0 else 4) if vec2.x >= 0 else (
        2 if vec2.y >= 0 else 3)
    if (quadrant_1 != quadrant_2):
        return False
    sin_angle = abs(vec1.x*vec2.y-vec1.y*vec2.x)
    return sin_angle < 0.0000000001


def compare_ccw_angle(vec1: Vector, vec2: Vector):
    quadrant_1 = (1 if vec1.y >= 0 else 4) if vec1.x >= 0 else (
        2 if vec1.y >= 0 else 3)
    quadrant_2 = (1 if vec2.y >= 0 else 4) if vec2.x >= 0 else (
        2 if vec2.y >= 0 else 3)
    if (quadrant_1 > quadrant_2):
        return 1
    elif (quadrant_1 < quadrant_2):
        return -1
    return -sign(vec1.x*vec2.y-vec1.y*vec2.x)


def l_ccw_angle(vec1: Vector, vec2: Vector):
    return True if compare_ccw_angle(vec1, vec2) == -1 else False


def lq_ccw_angle(vec1: Vector, vec2: Vector):
    return False if compare_ccw_angle(vec1, vec2) == 1 else True


def isBetween(p: Vector, q: Vector, r: Vector):
    if (is_collinear(p, q)):  # Тут может быть проблема
        return True
    if (l_ccw_angle(q, p)):
        # Тут может быть проблема
        return (l_ccw_angle(p, r) or lq_ccw_angle(r, q))
    else:
        # Тут может быть проблема
        return (l_ccw_angle(p, r) and lq_ccw_angle(r, q))


def draw_segments_sequence(segments):
    for segment in segments:
        plt.arrow(segment[0].x, segment[0].y, segment[1].x-segment[0].x, segment[1].y-segment[0].y,
                  shape='full', lw=0.5, length_includes_head=True, head_width=.05)
    plt.show()


def reduced_convolution(p1: Polygon, p2: Polygon):
    reduced_convolution = []
    n1 = len(p1.points)
    n2 = len(p2.points)

    if (n1 == 0 or n2 == 0):
        return []
    visited_states = set()
    state = Queue()
    for i in range(n1-1, -1, -1):
        state.put((i, 0))
    while (not state.empty()):
        current_state = state.get()
        i1 = current_state[0]
        i2 = current_state[1]
        if (current_state in visited_states):
            continue
        visited_states.add(current_state)

        next_i1 = p1.next_index(i1)
        next_i2 = p2.next_index(i2)
        prev_i1 = p1.prev_index(i1)
        prev_i2 = p2.prev_index(i2)

        for step in (True, False):
            new_i1 = 0
            new_i2 = 0
            if (step):
                new_i1 = next_i1
                new_i2 = i2
            else:
                new_i1 = i1
                new_i2 = next_i2
            belong_to_convolution = False
            if (step):
                belong_to_convolution = isBetween(
                    p1.point(next_i1)-p1.point(i1), p2.point(i2)-p2.point(prev_i2), p2.point(next_i2)-p2.point(i2))
            else:
                belong_to_convolution = isBetween(p2.point(next_i2)-p2.point(i2), p1.point(i1) -
                                                  p1.point(prev_i1), p1.point(next_i1)-p1.point(i1))
            if (belong_to_convolution):
                state.put((new_i1, new_i2))
                convex = False
                if (step):
                    convex = is_convex(p2.point(prev_i2),
                                       p2.point(i2), p2.point(next_i2))
                else:
                    convex = is_convex(p1.point(prev_i1),
                                       p1.point(i1), p1.point(next_i1))
                if (convex):
                    start_point = p1.point(i1)+p2.point(i2)
                    end_point = p1.point(new_i1)+p2.point(new_i2)
                    reduced_convolution.append((start_point, end_point))
    return reduced_convolution


def segment_intersection(segment1, segment2):
    A = (segment1[0].x, segment1[0].y)
    B = (segment1[1].x, segment1[1].y)

    C = (segment2[0].x, segment2[0].y)
    D = (segment2[1].x, segment2[1].y)

    line_1 = LineString([A, B])
    line_2 = LineString([C, D])
    int_pt = line_1.intersection(line_2)
    if int_pt:
        return Vector(int_pt.x, int_pt.y)


# Terrible function need rework
def split_by_intersections(reduce_conv):
    for i in range(len(reduce_conv)):
        for j in range(i+1, len(reduce_conv)):
            if not (reduce_conv[i][0] == reduce_conv[j][0] or reduce_conv[i][0] == reduce_conv[j][1] or reduce_conv[i][1] == reduce_conv[j][0] or reduce_conv[i][1] == reduce_conv[j][1]):
                intersection = segment_intersection(
                    reduce_conv[i], reduce_conv[j])
                if (intersection):
                    reduce_conv.insert(i+1, (intersection, reduce_conv[i][1]))
                    reduce_conv.insert(
                        j+2, (intersection, reduce_conv[j+1][1]))
                    reduce_conv[i] = (reduce_conv[i][0], intersection)
                    reduce_conv[j+1] = (reduce_conv[j+1][0], intersection)


def merge_polygons(poly1: Polygon, poly2: Polygon):
    segments = []
    for i in range(len(poly1.points)):
        segments.append((poly1.point(i), poly1.next(i)))
    for i in range(len(poly2.points)):
        segments.append((poly2.point(i), poly2.next(i)))
    split_by_intersections(segments)
    return segments


def minkowski_sum(poly1: Polygon, poly2: Polygon):
    reduce_conv = reduced_convolution(poly1, poly2)
    split_by_intersections(reduce_conv)
    arrangement = DCEL(reduce_conv)
    return arrangement.get_outer_boundary()


def get_max_point(poly: Polygon):
    max_point = poly.point(0)
    for point in poly.points:
        if max_point < point:
            max_point = point
    return max_point


def nfp(poly1: Polygon, poly2: Polygon):
    points = []

    for point in poly2.points:
        points.append(point*(-1))

    no_fit_polygon = minkowski_sum(poly1, Polygon(points))
    no_fit_polygon.move_to(
        poly2.minXY()+get_max_point(poly1)-get_max_point(no_fit_polygon))
    return no_fit_polygon


def pack(width, height, polygons: list[Polygon]):
    current_poly = polygons.pop()
    current_poly.move_to_origin()
    pallet = [current_poly]
    while (len(polygons) > 0):
        current_poly = polygons.pop()
        nfp_segments = [(Vector(0, 0), Vector(width, 0)), (Vector(width, 0.1), Vector(
            width, height)), (Vector(width, height), Vector(0.1, height)), (Vector(0, height), Vector(0, 0))]
        for polygon in pallet:
            no_fit_polygon = nfp(polygon, current_poly)
            for j in range(1, len(no_fit_polygon.points)):
                nfp_segments.append(
                    (no_fit_polygon.point(j), no_fit_polygon.next(j)))
        split_by_intersections(nfp_segments)
        arrangement = DCEL(nfp_segments)
        optimal_point = arrangement.get_optimal_point_in_area(width, height)
        current_poly.move_to(current_poly.minXY() +
                             optimal_point-current_poly.point(0))
        pallet.append(current_poly)
    return pallet


def get_orintable_loops(arrangement: Arrangement):


if __name__ == '__main__':
    # p1 = Polygon([Vector(0, 0), Vector(0, 1), Vector(2, 1),
    #              Vector(2, 3), Vector(3, 3), Vector(3, 0)])
    # p1.sort_points()
    # p2 = Polygon([Vector(0, 0), Vector(1, 1), Vector(0, 2), Vector(-1, 1)])
    # p2.sort_points()

    # p1 = Polygon([Vector(0, 0), Vector(1, 2), Vector(0, 1), Vector(-1, 2)])
    # p2 = Polygon([Vector(0, 0), Vector(-1, -2), Vector(0, -1), Vector(1, -2)])
    # p2.sort_points()
    # p1.draw()
    # p1 = Polygon([Vector(0, 0), Vector(10, 0), Vector(
    #    10, 5), Vector(6, 3), Vector(0, 3)])
    # p2 = Polygon([Vector(0, 0), Vector(-0.5, 3), Vector(5, 3),
    #             Vector(4.5, 1), Vector(4, 1.2)])
    # p1.sort_points()
    # p2.sort_points()
    # p1.draw()
    # p2.draw()
    # reduce_conv = reduced_convolution(p1, p2)
    # draw_segments_sequence(reduce_conv)
    # split_by_intersections(reduce_conv)
    # draw_segments_sequence(reduce_conv)
    # print(reduce_conv)

    poly1 = Polygon([Vector(0, 0), Vector(2, 0), Vector(2, 1), Vector(0, 1)])
    poly1.sort_points()
    poly2 = Polygon([Vector(0, 0), Vector(1, -3),
                     Vector(2, 0), Vector(1, 3)])
    poly2.sort_points()
    polygons = []

    for i in range(1):
        polygons.append(deepcopy(poly1))
        polygons.append(deepcopy(poly2))

    pallet = pack(2000, 1000, polygons)
    print(pallet)
