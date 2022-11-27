import math


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector({}, {})'.format(self.x, self.y)

    def __str__(self):  # print
        return '({}, {})'.format(self.x, self.y)

# ---------------------------  Computational operations   ---------------------------

    def __add__(self, other):  # +
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):  # +=
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):  # -
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):  # -=
        self.x -= other.x
        self.y -= other.y
        return self

    def __eq__(self, other):
        pt = self-other
        return (pt.x**2+pt.y**2) < 0.000001

    def __mul__(self, scalar):  # *
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):  # *
        return self*scalar

    def __imul__(self, scalar):  # *=
        self.x *= scalar
        self.y *= scalar
        return self

    def __itruediv__(self, scalar):  # /=
        self.x /= scalar
        self.y /= scalar
        return self

    def __abs__(self):  # длинна
        return math.hypot(self.x, self.y)

    def __bool__(self):  # преверка на == (0,0)
        return self.x != 0 or self.y != 0

    def __neg__(self):  # -
        return Vector(-self.x, -self.y)

    def __lt__(self, other):  # лексикографический порядок
        return (self.y < other.y) or ((self.y == other.y) and self.x < other.x)

    def to_tuple(self):
        return (self.x, self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

# ---------------------------  Geometric operations   ---------------------------

    def angle(self):
        """[0;2pi)"""
        if abs(self) == 0:
            return 0.0
        fi1 = math.acos(self.x / abs(self))
        fi2 = math.asin(self.y / abs(self))
        answer = 0
        if fi1 < math.pi / 2:
            answer = fi2
        elif fi2 > 0:
            answer = fi1
        else:
            answer = -fi1
        if answer < 0:
            answer += 2 * math.pi
        return answer

    def get_orthogonal(self):
        return Vector(self.y, -self.x).normalize()

    def normalize(self):
        if abs(self) != 0:
            len = abs(self)
            self.x /= len
            self.y /= len
        return self

    def rotate(self, angle):
        a = self.x
        b = self.y
        self.x = a * math.cos(angle) - b * math.sin(angle)
        self.y = a * math.sin(angle) + b * math.cos(angle)
        return self

    @staticmethod
    def is_collinear(vec1: 'Vector', vec2: 'Vector'):
        quadrant_1 = (1 if vec1.y >= 0 else 4) if vec1.x >= 0 else (
            2 if vec1.y >= 0 else 3)
        quadrant_2 = (1 if vec2.y >= 0 else 4) if vec2.x >= 0 else (
            2 if vec2.y >= 0 else 3)
        if (quadrant_1 != quadrant_2):
            return False
        sin_angle = abs(vec1.x*vec2.y-vec1.y*vec2.x)
        return sin_angle < 0.0000000001

    def copy(self):
        return Vector(self.x, self.y)

    def angle(self):
        """[0;2pi)"""
        if abs(self) == 0:
            return 0
        fi1 = math.acos(self.x / abs(self))
        fi2 = math.asin(self.y / abs(self))
        answer = 0
        if fi1 < math.pi / 2:
            answer = fi2
        elif fi2 > 0:
            answer = fi1
        else:
            answer = -fi1
        if answer < 0:
            answer += 2 * math.pi
        return answer

    def is_horizontal(self, other):
        return self.y == other.y

    def is_vertical(self, other):
        return self.x == other.x


if __name__ == "__main__":
    a = Vector(1.0001, 2)
    b = Vector(1, 2)
    print(type(b.x))
    print(b*2)
    print(2*b)
    print(b)
    b /= 2*2
    print(b)
    print(Vector.is_collinear(a, b))
