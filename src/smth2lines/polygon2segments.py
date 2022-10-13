from math import ceil, floor

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
    size_of_sides = shift2zero(points)
    n_x = ceil(size_of_sides[0] / h)
    n_y = ceil(size_of_sides[1] / h)

    lines = []
    for _ in range(n_y + 1):
        lines.append([])

    for k in range(0, n_y + 1):
        print('hello', k)
        for i0 in range(points.shape[0]):
            if i0 == points.shape[0] - 1:
                i1 = 0
            else:
                i1 = (i0 + 1)
            if i0 == 0:
                i2 = points.shape[0] - 1
            else:
                i2 = (i0 - 1)
            # вершина лежит на линии
            if points[i0][1] == k * h:
                if points[i2][1] < k * h and points[i1][1] < k * h:
                    lines[k].append(points[i0][0])
                    lines[k].append(points[i0][0])
                elif points[i2][1] > k * h and points[i1][1] > k * h:
                    lines[k].append(points[i0][0])
                    lines[k].append(points[i0][0])
                else:
                    lines[k].append(points[i0][0])
            # ребро пересекает линию
            if points[i0][1] < k * h < points[i1][1] or points[i1][1] < k * h < points[i0][1]:
                # print(i0, k)
                lines[k].append(intersection([points[i0], points[i1]], [[0, k * h], [n_x, k * h]])[0])
                # print(intersection([points[i0], points[i1]], [[0, k * h], [n_x, k * h]])[0])
            # extension algorithm
            if k * (h + 1) > points[i0][1] > k * h >= points[i1][1] and points[i2][1] <= k * h:
                lines[k + 1].append(points[i0][0])
                lines[k + 1].append(points[i0][0])
            elif points[i1][1] >= k * h > points[i0][1] > k * (h + 1) and points[i2][1] >= k * h:
                lines[k + 1].append(points[i0][0])
                lines[k + 1].append(points[i0][0])

    return lines

if __name__=='__main__':
    print(polygon2segments(np.array([[1, 0], [0.3, 3], [3, 3.7], [2.1, 0]]), 2.6))