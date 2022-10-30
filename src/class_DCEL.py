from numpy import half, sign
from class_polygon import Polygon
from class_vector import Vector
from enum import Enum


def compare_ccw_angle(vec1: Vector, vec2: Vector):
    quadrant_1 = (1 if vec1.y >= 0 else 4) if vec1.x >= 0 else (
        2 if vec1.y >= 0 else 3)
    quadrant_2 = (1 if vec2.y >= 0 else 4) if vec2.x >= 0 else (
        2 if vec2.y >= 0 else 3)
    if (quadrant_1 > quadrant_2):
        return 1
    elif (quadrant_1 < quadrant_2):
        return -1
    return -sign(vec1.x*vec2.y-vec1.y*vec2.x)


def l_ccw_angle(vec1: Vector, vec2: Vector):
    return True if compare_ccw_angle(vec1, vec2) == -1 else False


def lq_ccw_angle(vec1: Vector, vec2: Vector):
    return False if compare_ccw_angle(vec1, vec2) == 1 else True


def psevdoProd(p1: Vector, p2: Vector):
    return p1.x*p2.y-p1.y*p2.x


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


class Vertex:
    def __init__(self, point: Vector):
        self.point = point
        self.half_edges_by_ccw_angle: list[HalfEdge] = []

    def add_half_edge(self, half_edge):
        for i in range(len(self.half_edges_by_ccw_angle)):
            if (self.half_edges_by_ccw_angle[i].direction > half_edge.direction):
                self.half_edges_by_ccw_angle.insert(i-1, half_edge)
                return
        self.half_edges_by_ccw_angle.append(half_edge)


class HalfEdge:
    def __init__(self):
        self.original_edge: tuple[Vector, Vector] = None
        self.origin: Vector = None
        self.end: Vector = None
        self.twin: HalfEdge = None
        self.face: Face = None
        self.prev: HalfEdge = None
        self.next: HalfEdge = None
        self.direction: Direction = None
        self.hole_begining: HalfEdge = None

    @staticmethod
    def init_pair_halfedges(edge: tuple[Vector, Vector]):

        half_edge = HalfEdge()
        twin_half_edge = HalfEdge()

        half_edge.original_edge = edge
        twin_half_edge.original_edge = edge

        half_edge.twin = twin_half_edge
        twin_half_edge.twin = half_edge

        half_edge.origin = edge[0]
        half_edge.end = edge[1]

        twin_half_edge.origin = edge[1]
        twin_half_edge.end = edge[0]

        half_edge.direction = Direction(edge[1]-edge[0])
        twin_half_edge.direction = Direction(edge[0]-edge[1])

        return half_edge, twin_half_edge


class Face:
    def __init__(self, half_edge=None):
        self.boundary_half_edge: HalfEdge = half_edge
        self.holes_half_edges: list[HalfEdge] = []

    def is_inside(self, point):
        if (self.boundary_half_edge is None):
            return True
        start_boundary_half_edge = self.boundary_half_edge
        current_boundary_half_edge = self.boundary_half_edge
        # Если не лежит слева от полуребра
        while (current_boundary_half_edge != start_boundary_half_edge):
            if (psevdoProd(current_boundary_half_edge.end - current_boundary_half_edge.origin,
                           point-current_boundary_half_edge.origin) < 0):
                return False
        return True

    def get(self) -> Polygon:
        start = self.boundary_half_edge
        current = self.boundary_half_edge.next
        if (current == None or start == current):
            return None
        poly = [start.origin]
        while (start != current):
            poly.append(current.origin)
            current = current.next
        return Polygon(poly)


class DCEL:
    def __init__(self) -> None:
        self.unbounded_face: Face = Face()
        self.faces: list[Face] = [self.unbounded_face]
        self.vertices: dict[Vector, Vertex] = dict()
        self.half_edges: list[HalfEdge] = []

    def add_edge(self, edge: tuple[Vector, Vector]):
        half_edge, twin_half_edge = HalfEdge.init_pair_halfedges(edge)

        is_origin_edge_incendent = edge[0] in self.vertices
        is_end_edge_incendent = edge[0] in self.vertices

        match (is_origin_edge_incendent, is_end_edge_incendent):

            case (False, False):  # NO_INCENDENT_VERTEX
                self.add_without_incendent_vertex(half_edge, twin_half_edge)

                face = self.get_face_by_inside_point(half_edge.origin)
                face.holes_half_edges.append(half_edge)

                half_edge.hole_begining = half_edge
                twin_half_edge.hole_begining = twin_half_edge

                half_edge.face = face
                twin_half_edge.face = face

            case (True, False):  # ONLY_ORIGIN_VERTEX_INCENDENT
                self.add_half_edge_with_incendent_vertex(half_edge)
                end_vertex = Vertex(edge[1])
                end_vertex.add_half_edge(twin_half_edge)
                self.vertices[edge[1]] = end_vertex

                half_edge.hole_begining = half_edge.prev.hole_begining
                half_edge.face = half_edge.prev.face

                twin_half_edge.hole_begining = half_edge.prev.twin.hole_begining
                twin_half_edge.face = half_edge.prev.twin.face

            case (False, True):  # ONLY_END_VERTEX_INCENDENT
                self.add_half_edge_with_incendent_vertex(twin_half_edge)
                origin_vertex = Vertex(edge[0])
                origin_vertex.add_half_edge(half_edge)
                self.vertices[edge[0]] = origin_vertex

                twin_half_edge.hole_begining = twin_half_edge.prev
                twin_half_edge.face = twin_half_edge.prev.face

                half_edge.hole_begining = twin_half_edge.prev.twin.hole_begining
                half_edge.face = twin_half_edge.prev.twin.face

            case (False, False):  # BOTH_VERTEX_INCENDENT
                self.add_half_edge_with_incendent_vertex(half_edge)
                self.add_half_edge_with_incendent_vertex(twin_half_edge)

                # Connect two holes case (All cases with degenerates and non-degenerates cases)
                if (half_edge.next.hole_begining != half_edge.prev.hole_begining):
                    half_edge.face = half_edge.prev.face
                    twin_half_edge.face = twin_half_edge.prev.face

                    half_edge.hole_begining = half_edge.prev.hole_begining
                    twin_half_edge.hole_begining = twin_half_edge.prev.hole_begining

                elif (half_edge.next.face != half_edge.next.twin.face):  # Splite face case
                    half_edge.hole_begining = None
                    twin_half_edge.hole_begining = None

                    new_face = Face()
                    new_face.boundary_half_edge = half_edge

                    half_edge.face = half_edge
                    current_half_edge = half_edge.next

                    while (current_half_edge != half_edge):
                        current_half_edge.face = half_edge
                        current_half_edge = current_half_edge.next

                    self.faces.append(face)
                else:  # loop closure case
                    new_face = Face()
                    start_half_edge = half_edge
                    current_half_edge = half_edge.next

                    half_edge.face = half_edge.next.face  # pre init faces
                    twin_half_edge.face = half_edge.next.face

                    while (current_half_edge != half_edge):
                        if (current_half_edge.orgin < start_half_edge.origin):
                            start_half_edge = current_half_edge
                    if (psevdoProd(start_half_edge.origin - start_half_edge.prev.origin, start_half_edge.end - start_half_edge.prev.origin) < 0):  # check orientation
                        start_half_edge = start_half_edge.twin.next

                    start_half_edge.face = new_face
                    start_half_edge.hole_begining = None

                    current_half_edge = start_half_edge.next
                    while (start_half_edge != current_half_edge):
                        current_half_edge.face = new_face
                        current_half_edge.hole_begining = None

                    self.faces.append(new_face)

        self.half_edges.append(half_edge)
        self.half_edges.append(twin_half_edge)

    def add_without_incendent_vertex(self, half_edge: HalfEdge, twin_half_edge: HalfEdge):
        origin_vertex = Vertex(half_edge.original_edge[0])
        origin_vertex.add_half_edge(half_edge)

        end_vertex = Vertex(twin_half_edge.original_edge[1])
        end_vertex.add_half_edge(twin_half_edge)

        half_edge.next = twin_half_edge
        half_edge.prev = twin_half_edge

        twin_half_edge.next = half_edge
        twin_half_edge.prev = half_edge

        self.vertices[half_edge.origin] = origin_vertex
        self.vertices[twin_half_edge.origin] = end_vertex

    def add_half_edge_with_incendent_vertex(self, half_edge: HalfEdge):
        incendent_vertex = self.vertices[half_edge.origin]
        incendent_vertex.add_half_edge(half_edge)
        half_edge_index = incendent_vertex.half_edges_by_ccw_angle.index(
            half_edge)

        size = len(incendent_vertex.half_edges_by_ccw_angle)
        left_half_edge = incendent_vertex.half_edges_by_ccw_angle[(  # by ccw angle
            half_edge_index+1) % size]
        right_half_edge = incendent_vertex.half_edges_by_ccw_angle[(  # by ccw angle
            half_edge_index-1) % size]

        right_half_edge.prev = half_edge.twin
        half_edge.twin.next = right_half_edge

        left_half_edge.twin.next = half_edge
        half_edge.prev = left_half_edge.twin

        if (half_edge.next == None):
            half_edge.next = half_edge.twin

    def get_face_by_inside_point(self, point: Vector):
        face = self.unbounded_face
        for current_face in self.faces:
            if (current_face.boundary_half_edge is None):
                continue
            if (current_face.is_inside(point) and face.is_inside(current_face.boundary_half_edge.origin)):
                face = current_face
        return current_face

    def init_faces(self):
        for half_edge in self.half_edges:
            if (half_edge.face is None):
                double_signed_area = 0
                current_half_edge = half_edge.next

                while (half_edge != current_half_edge):
                    p1 = current_half_edge.prev.origin
                    p2 = current_half_edge.origin
                    p3 = current_half_edge.end

                    double_signed_area += psevdoProd(p2-p1, p3-p1)


if __name__ == '__main__':
    segments = [(Vector(0, 0), Vector(0, 1)), (Vector(0, 1), Vector(1, 1)), (Vector(
        1, 1), Vector(1, 0)), (Vector(1, 0), Vector(0, 0)), (Vector(0, 0), Vector(0.5, 0.5))]
    arrangement = DCEL()
    for segment in segments:
        arrangement.add_edge(segment)

    poly = arrangement
    print()
