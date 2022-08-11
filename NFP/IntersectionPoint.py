from __future__ import division

import numpy as np


def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C


def intersection_point(edge1, edge2):
    """"
    Function to count the point of intersection of two lines
    """
    points1 = np.array([edge1.coordinate, edge1.edges[0]])
    points2 = np.array([edge2.coordinate, edge2.edges[0]])
    L1 = line(points1[0], points1[1])
    L2 = line(points2[0], points2[1])
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return [x, y]
    else:
        return False

