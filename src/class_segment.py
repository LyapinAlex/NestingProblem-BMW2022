from numpy import sign
from class_direction import is_collinear, psevdoProd

from class_vector import Vector


class Segment:
    def __init__(self, a: Vector, b: Vector, id) -> None:
        self.a = a
        self.b = b
        self.min_point = min(a, b)
        self.max_point = max(a, b)
        self.id = id

    def __eq__(self, other):  # ==
        return self.min_point == other.min_point and self.max_point == other.max_point

    def __lt__(self, other):  # <
        return (self.min_point < other.min_point) or ((self.min_point == other.min_point) and
                                                      (self.max_point < other.max_point))

    def __le__(self, other):  # <=
        return self < other or self == other

    def __hash__(self) -> int:
        return hash((self.min_point, self.max_point))

    def compare_with_point(self, point):  # Проверить
        a = self.max_point - self.min_point
        b = point - self.min_point
        signed_area = psevdoProd(a, b)
        return sign(signed_area)

    @staticmethod
    def intersection(this: 'Segment', other: 'Segment'):  # Проверить
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
                    return (this.min_point + a * l1).round()
        return None

    def distance_point_from_segment(self, point: Vector):
        a = self.max_point - self.min_point
        b = point - self.min_point
        return psevdoProd(a, b)
