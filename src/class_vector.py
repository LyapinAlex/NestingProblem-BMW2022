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

    def __mul__(self, scalar): # *
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar): # *
        return self*scalar

    def __imul__(self, scalar): # *=
        self.x *= scalar
        self.y *= scalar
        return self

    def __itruediv__(self, scalar): # /=
        self.x /= scalar
        self.y /= scalar
        return self

    def __abs__(self):  # длинна
        return math.hypot(self.x, self.y)

    def __bool__(self):  # преверка на == (0,0)
        return self.x != 0 or self.y != 0

    def __neg__(self):  # -
        return Vector(-self.x, -self.y)

    def __lt__(self, other): #лексикографический порядок
        return (self.y < other.y) or ((self.y == other.y) and self.x < other.x)

    def to_tuple(self):
        return (self.x, self.y)

# ---------------------------  Geometric operations   ---------------------------

    def angle(self):
        """[0;2pi)"""
        if abs(self)==0: return 0.0
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
        if abs(self)!=0:
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

    def is_collinear(self, other):
        angle_difference = abs(self.angle() - other.angle())
        if angle_difference > math.pi: angle_difference-=math.pi
        return angle_difference < 0.0001

    def copy(self):
        return Vector(self.x, self.y)


if __name__ == "__main__":
    a = Vector(1.0001, 2)
    b = Vector(1, 2)
    print(type(b.x))
    print(b*2)
    print(2*b)
    print(b)
    b/=2*2
    print(b)
    print(a.is_collinear(b))