from math import ceil, floor

from copy import copy

# if __name__=='__main__':
#     from shift2zero import shift2zero
# else:
#     from .shift2zero import shift2zero
import numpy as np

from src.smth2matrix.shift2zero import shift2zero


def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(points1, points2):
    L1 = line(points1[0], points1[1])
    L2 = line(points2[0], points2[1])
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False


def polygon2segments(points, h):

    shift2zero(points)

    n_x1 = 0
    n_y1 = 0
    for point in points:
        if point[0] > n_x1:
            n_x1 = copy(point[0])
        if point[1] > n_y1:
            n_y1 = copy(point[1])
    n_x = ceil(n_x1 / h)
    n_y = ceil(n_y1 / h)

    lines = []
    for _ in range(n_y + 1):
        lines.append([])


    for k in range(0, n_y + 1):
        start = None
        end = None
        intersection_start = None
        intersection_end = None
        counter = 0
        i0 = 0
        while i0 < len(points):
            if i0 == len(points) - 1:
                i1 = 0
            else:
                i1 = (i0 + 1)
            if i0 == 0:
                i2 = len(points) - 1
            else:
                i2 = (i0 - 1)

            # вершина лежит на линии
            if points[i0][1] == k * h:
                if points[i2][1] < k * h and points[i1][1] < k * h:
                    lines[k].append([points[i0][0], points[i0][0]])
                elif points[i2][1] > k * h and points[i1][1] > k * h:
                    lines[k].append([points[i0][0], points[i0][0]])
                else:
                    if start is None:
                        start = copy(points[i0][0])
                    else:
                        end = copy(points[i0][0])

            # ребро пересекает линию
            elif points[i0][1] < k * h < points[i1][1] or points[i1][1] < k * h < points[i0][1]:
                intersection_point = intersection([points[i0], points[i1]], [[0, k * h], [n_x, k * h]])[0]
                if start is None:
                    start = copy(intersection_point)
                else:
                    end = copy(intersection_point)
            if end is not None:
                lines[k].append([start, end])
                start = None
                end = None
            i0 += 1

    # print(lines)

    k_prev = 0
    k_next = 0
    point_prev = None
    point_next = None
    for k in range(0, n_y + 1):
        min = n_x1
        max = 0
        i0 = 0
        while i0 < 2 * len(points):
            if i0 < len(points):
                i = i0
            else:
                i = len(points) - i0
            if i == len(points):
                i = -1
            if i == len(points) - 1:
                i_next = 0
            else:
                i_next = (i + 1)
            if i == 0:
                i_prev = len(points) - 1
            else:
                i_prev = (i - 1)
            if (k + 1) * h >= points[i][1] > k * h >= points[i_prev][1] or k * h < points[i][1] <= (k + 1) * h <= \
                    points[i_prev][1]:
                # print('case1', points[i], k)
                if points[i_prev][1] <= k * h:
                    k_prev = -1
                    k_next = 0
                    intersection_point = intersection([points[i_prev], points[i]], [[0, k * h], [n_x, k * h]])[0]
                    point_prev = copy(intersection_point)
                    point_next = None
                    if max < points[i][0]:
                        max = copy(points[i][0])
                    if min > points[i][0]:
                        min = copy(points[i][0])
                    # print(min, max)
                elif points[i_prev][1] >= (k + 1) * h:
                    k_prev = 1
                    k_next = 0
                    intersection_point = \
                    intersection([points[i_prev], points[i]], [[0, (k + 1) * h], [n_x, (k + 1) * h]])[0]
                    point_prev = copy(intersection_point)
                    point_next = None
                    if max < points[i][0]:
                        max = copy(points[i][0])
                    if min > points[i][0]:
                        min = copy(points[i][0])
                    # print(points[i], min, max)
            elif points[i][1] <= k * h < points[i_prev][1] <= (k + 1) * h or k * h < points[i_prev][1] <= (
                    k + 1) * h and points[i][1] >= (k + 1) * h:
                # print('case2', points[i], k)
                if points[i][1] <= k * h:
                    k_next = -1
                    intersection_point = intersection([points[i_prev], points[i]], [[0, k * h], [n_x, k * h]])[0]
                    point_next = copy(intersection_point)
                elif points[i][1] >= (k + 1) * h:
                    k_next = 1
                    intersection_point = \
                    intersection([points[i_prev], points[i]], [[0, (k + 1) * h], [n_x, (k + 1) * h]])[0]
                    point_next = copy(intersection_point)
            elif k * h < points[i][1] <= (k + 1) * h and k * h < points[i_prev][1] <= (k + 1) * h:
                if max < points[i][0]:
                    max = copy(points[i][0])
                if min > points[i][0]:
                    min = copy(points[i][0])
                i0 += 1
                continue
            if k_prev * k_next != 0:
                if k_prev * k_next == 1 and not (i==0 and i0==0):
                    if k_prev == -1:
                        k_prev = 0
                        k_next = 0
                        lines[k + 1].append([min, max])
                        if min < point_prev and min < point_next:
                            if point_prev < point_next:
                                lines[k].append([min, point_prev])
                            elif point_next < point_prev:
                                lines[k].append([min, point_next])
                        if max > point_prev and max > point_next:
                            if point_prev > point_next:
                                lines[k].append([point_prev, max])
                            elif point_next > point_prev:
                                lines[k].append([point_next, max])
                        min = n_x1
                        max = 0
                    if k_prev == 1:
                        k_prev = 0
                        k_next = 0
                        lines[k].append([min, max])
                        if min < point_prev and min < point_next:
                            if point_prev < point_next:
                                lines[k + 1].append([min, point_prev])
                            elif point_next < point_prev:
                                lines[k + 1].append([min, point_next])
                        if max > point_prev and max > point_next:
                            if point_prev > point_next:
                                lines[k + 1].append([point_prev, max])
                            elif point_next > point_prev:
                                lines[k + 1].append([point_next, max])
                        min = n_x1
                        max = 0
                elif k_prev * k_next == -1:
                    if k_prev == -1:
                        if min < point_prev:
                            lines[k].append([min, point_prev])
                        if max > point_prev:
                            lines[k].append([point_prev, max])
                        if min < point_next:
                            lines[k + 1].append([min, point_next])
                        if max > point_next:
                            lines[k + 1].append([point_next, max])
                        k_prev = 0
                        k_next = 0
                        min = n_x1
                        max = 0
                    elif k_prev == 1:
                        # print('case1', [min, max], [point_prev, point_next])
                        if min < point_prev:
                            # print('1', [min, point_prev])
                            lines[k + 1].append([min, point_prev])
                        if max > point_prev:
                            # print('2', [point_prev, max])
                            lines[k + 1].append([point_prev, max])
                        if min < point_next:
                            # print('3', [min, point_next])
                            lines[k].append([min, point_next])
                        if max > point_next:
                            # print('4', [point_next, max])
                            lines[k].append([point_next, max])
                        k_prev = 0
                        k_next = 0
                        min = n_x1
                        max = 0
                k_prev = 0
                k_next = 0
            i0 += 1

    def first_elem(e):
        return e[0]

    for line in lines:
        for segment in line:
            segment.sort()
        line.sort(key=first_elem)
        i = 0
        while i < (len(line) - 1):
            if line[i][1] == line[i + 1][0]:
                line[i][1] = line[i + 1][1]
                line.pop(i + 1)
                continue
            if line[i][1] > line[i + 1][0]:
                if line[i][1] < line[i + 1][1]:
                    line[i][1] = line[i + 1][1]
                    line.pop(i + 1)
                    continue
            if line[i][1] > line[i + 1][0]:
                if line[i][1] >= line[i + 1][1]:
                    line.pop(i + 1)
                    continue
            i += 1

    return lines

# if __name__=='__main__':
#     print(polygon2segments(np.array([[1, 0], [0.3, 3], [3, 3.7], [2.1, 0]]), 2.6))