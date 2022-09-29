import math


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({}, {})'.format(self.x, self.y)

    def __str__(self):  # print
        return '({}, {})'.format(self.x, self.y)

    def __add__(self, other):  # +
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):  # +=
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):  # -
        return Point(self.x - other.x, self.y - other.y)

    def __isub__(self, other):  # -=
        self.x -= other.x
        self.y -= other.y
        return self

    def __abs__(self):  # длинна
        return math.hypot(self.x, self.y)

    def __bool__(self):  # преверка на == (0,0)
        return self.x != 0 or self.y != 0

    def __neg__(self):  # отражение относительно начала координат
        return Point(-self.x, -self.y)

    def to_tuple(self):
        return (self.x, self.y)

    def rotate(self, angle):
        a = self.x
        b = self.y
        self.x = a * math.cos(angle) - b * math.sin(angle)
        self.y = a * math.sin(angle) + b * math.cos(angle)
        return self

    def angle(self):
        fi1 = math.acos(self.x/abs(self))
        fi2 = math.asin(self.y/abs(self))
        return fi1, fi2


if __name__ == "__main__":
    a = Point(1, -2)
    print(a.angle())