import math

_NDIGITS = 6
_ANGLE_ERROR = 0.0001
_LENGTH_ERROR = 0.000001

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector({}, {})'.format(self.x, self.y)

    def __str__(self):  # print
        return '({}, {})'.format(self.x, self.y)

    def to_tuple(self):
        return (self.x, self.y)

    def copy(self):
        return Vector(self.x, self.y)

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

    def __mul__(self, scalar):  # *
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):  # *
        return self * scalar

    def __imul__(self, scalar):  # *=
        self.x *= scalar
        self.y *= scalar
        return self

    def __itruediv__(self, scalar):  # /=
        self.x /= scalar
        self.y /= scalar
        return self

    def __neg__(self):  # -
        return Vector(-self.x, -self.y)

# ----------------------------  Logical operations   ----------------------------
# лексикографический порядок

    def __bool__(self):  # != Vector(0,0)
        return self.x != 0 or self.y != 0

    def __eq__(self, other): # ==
        return (self.x == other.x) and (self.y == other.y)

    def __lt__(self, other):  # <
        return (self.y < other.y) or ((self.y == other.y) and self.x < other.x)

    def __le__(self, other):  # <=
        return self < other or self == other

# ---------------------------  Geometric operations   ---------------------------

    def __abs__(self):  # длинна
        return math.hypot(self.x, self.y)

    def angle(self):
        """[0;2pi)"""
        if abs(self) == 0: return 0.0
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

    def rotate(self, angle):
        a = self.x
        b = self.y
        self.x = a * math.cos(angle) - b * math.sin(angle)
        self.y = a * math.sin(angle) + b * math.cos(angle)
        return self

    def normalize(self):
        if abs(self) != 0:
            len = abs(self)
            self.x /= len
            self.y /= len
        return self

    def in_neighborhood_zero(self):
        return abs(self) <= _LENGTH_ERROR

    def is_collinear(self, other):
        angle_difference = abs(self.angle() - other.angle())
        if angle_difference > math.pi: angle_difference -= math.pi
        return angle_difference <= _ANGLE_ERROR

    def psevdo_prod(self, other):
        return self.x * other.y - self.y * other.x

    def round(self, ndigits = _NDIGITS):
        self.x = round(self.x, ndigits)
        self.y = round(self.y, ndigits)
        return self


def intersection_pair_segments(p1: Vector, p2: Vector, q1: Vector, q2: Vector):
    a = p2 - p1
    b = q1 - q2
    c = q1 - p1
    if a.psevdo_prod(b):
        l1 = c.psevdo_prod(b) / a.psevdo_prod(b)
        l2 = a.psevdo_prod(c) / a.psevdo_prod(b)
        if (0<=l1) and (l1<=1) and (0<=l2) and (l2<=1):
            return p1+a*l1
    return None


if __name__ == "__main__":
    # a2 = Vector(2, 2)
    # a1 = Vector(1, 1)
    # b2 = Vector(2, 1.5)
    # b1 = Vector(1, 2)
    # print(intersection_pair_segments(a1, a2, b1, b2))
    a = Vector(27.552853668126623, 3.3332999999)
    b = Vector(2, 1)
    c = Vector(1, 2)
    d = Vector(2, 2)
    print(a.round())
