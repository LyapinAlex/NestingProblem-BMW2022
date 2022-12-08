from numpy import sign
from class_direction import is_collinear, psevdoProd

from class_vector import Vector


class Segment:
    def __init__(self, a: Vector, b: Vector) -> None:
        self.a = a
        self.b = b
        self.min_point = min(a, b)
        self.max_point = max(a, b)

    def __eq__(self, other):  # ==
        return self.min_point == other.min_point and self.max_point == other.max_point

    def __lt__(self, other):  # <
        return self != other and (self.min_point < other.min_point) or ((self.min_point == other.min_point) and
                                                                        (self.max_point < other.max_point))

    def __le__(self, other):  # <=
        return self < other or self == other

    def __hash__(self) -> int:
        return hash((self.min_point, self.max_point))

    def compare_with_point(self, point):  # Проверить
        a = self.max_point - self.min_point
        b = point - self.min_point
        if (is_collinear(a, b) or a == Vector(0, 0) or b == Vector(0, 0)):
            return 0
        signed_area = psevdoProd(a, b)
        if (abs(signed_area) < 0.000001):
            return 0
        return sign(signed_area)

    @staticmethod
    # TODO: Проверить и сделать чтобы работало для пересечений при касании по внутренности
    def intersection(this: 'Segment', other: 'Segment'):
        """Возвращает координату пересечения пары отрезков, но\\
            если отрезки параллельны или хотя бы одна из возможных пар из их концов совпадает возвращает None"""
        a = this.max_point - this.min_point
        b = other.min_point - other.max_point
        c = other.min_point - this.min_point
        if psevdoProd(a, b):
            l1 = psevdoProd(c, b) / psevdoProd(a, b)
            l2 = psevdoProd(a, c) / psevdoProd(a, b)
            if (0 <= l1) and (l1 <= 1) and (0 <= l2) and (l2 <= 1):
                if (0 == l1 and (0 == l2 or l2 == 1)) or (1 == l1 and (0 == l2 or l2 == 1)):
                    return None
                else:
                    return this.min_point + a * l1
        return None

    def distance_point_from_segment(self, point: Vector):
        a = self.max_point - self.min_point
        b = point - self.min_point
        return psevdoProd(a, b)


if __name__ == '__main__':
    s1 = Segment(Vector(0, 0), Vector(1, 0), 0)
    s2 = Segment(Vector(0.5, 0), Vector(0.5, 1), 1)
    intersection = Segment.intersection(s2, s1)
    print(intersection)
