import math
from numpy import sign
from class_vector import Vector


def compare_ccw_angle(vec1: Vector, vec2: Vector):
    quadrant_1 = (1 if vec1.y >= 0 else 4) if vec1.x >= 0 else (
        2 if vec1.y >= 0 else 3)
    quadrant_2 = (1 if vec2.y >= 0 else 4) if vec2.x >= 0 else (
        2 if vec2.y >= 0 else 3)
    if (quadrant_1 > quadrant_2):
        return 1
    elif (quadrant_1 < quadrant_2):
        return -1
    if (abs(vec1.x*vec2.y-vec1.y*vec2.x) < 0.0000000001):
        return 0
    return -sign(vec1.x*vec2.y-vec1.y*vec2.x)


def is_collinear(vec1: Vector, vec2: Vector):
    quadrant_1 = (1 if vec1.y >= 0 else 4) if vec1.x >= 0 else (
        2 if vec1.y >= 0 else 3)
    quadrant_2 = (1 if vec2.y >= 0 else 4) if vec2.x >= 0 else (
        2 if vec2.y >= 0 else 3)
    if (quadrant_1 != quadrant_2):
        return False
    sin_angle = abs(vec1.x*vec2.y-vec1.y*vec2.x)
    return sin_angle < 0.0000000001


def isBetween(p: Vector, q: Vector, r: Vector):
    if (is_collinear(p, q) or is_collinear(p, r)):  # Мутная тема
        return True
    if (l_ccw_angle(q, p)):
        return (l_ccw_angle(p, r)) or lq_ccw_angle(r, q)
    else:
        return (l_ccw_angle(p, r) and lq_ccw_angle(r, q))


def l_ccw_angle(vec1: Vector, vec2: Vector):
    return True if compare_ccw_angle(vec1, vec2) == -1 else False


def lq_ccw_angle(vec1: Vector, vec2: Vector):
    return False if compare_ccw_angle(vec1, vec2) == 1 else True


def psevdoProd(p1: Vector, p2: Vector):
    return p1.x*p2.y-p1.y*p2.x


def is_convex(p1: Vector, p2: Vector, p3: Vector):
    return psevdoProd(p2-p1, p3-p2) > 0.0000000000000001


class Direction:
    def __init__(self, vector: Vector) -> None:
        self.direction = vector

    def __lt__(self, other):  # Counter clockwise angle
        return l_ccw_angle(self.direction, other.direction)

    def __ltq__(self, other):  # Counter clockwise angle
        return lq_ccw_angle(self.direction, other.direction)

    def __gt__(self, other):
        return l_ccw_angle(other.direction, self.direction)

    def __gtq__(self, other):
        return lq_ccw_angle(other.direction, self.direction)
