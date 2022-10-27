

from numpy import sign
from class_polygon import Polygon

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
    return -sign(vec1.x*vec2.y-vec1.y*vec2.x)


def l_ccw_angle(vec1: Vector, vec2: Vector):
    return True if compare_ccw_angle(vec1, vec2) == -1 else False


def lq_ccw_angle(vec1: Vector, vec2: Vector):
    return False if compare_ccw_angle(vec1, vec2) == 1 else True


class Vertex:
    def __init__(self, point: Vector, half_edge):
        self.point = point
        self.half_edge: HalfEdge = half_edge

    def incendent_edges(self):
        start_edge = self.half_edge
        current = start_edge.twin.next
        edges = [(start_edge.origin, start_edge.end)]
        while (current != start_edge):
            edges.append((current.origin, current.end))
            current = current.twin.next
        return edges


class Face:
    def __init__(self, half_edge):
        self.boundary_half_edge: HalfEdge = half_edge
        self.holes_half_edges: list[HalfEdge] = []

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

    def is_closed(self):
        start_half_edge = self.boundary_half_edge
        current_half_edge = start_half_edge.next
        if ((start_half_edge.next == None or start_half_edge.prev == None) or
                (current_half_edge.next == current_half_edge.twin and current_half_edge.prev == current_half_edge.twin)):
            return False
        while (current_half_edge != start_half_edge and current_half_edge != None):
            current_half_edge = current_half_edge.next
        return not current_half_edge == None


class HalfEdge:
    def __init__(self, edge: tuple[Vector, Vector]):
        self.origin: Vector = edge[0]
        self.end: Vector = edge[1]
        self.twin: HalfEdge = None
        self.face: Face = None
        self.prev: HalfEdge = None
        self.next: HalfEdge = None
        self.direction = edge[1]-edge[0]

    def is_degenerate(self):
        return self.next == self.twin or self.prev == self.twin


class DCEL:
    def __init__(self, edges: tuple[Vector, Vector]):
        self.faces: list[Face] = []
        self.vertices: dict[Vector, Vertex] = dict()  # binary tree
        self.half_edges: list[HalfEdge] = []

        for edge in edges:
            self.add_edge(edge)
        self.init_faces()
        # self.remove_degenerate_cases()

    def add_edge(self, edge):

        half_edge = HalfEdge(edge)
        twin_half_edge = HalfEdge((edge[1], edge[0]))
        half_edge.twin = twin_half_edge
        twin_half_edge.twin = half_edge

        if (edge[0] not in self.vertices and edge[1] not in self.vertices):
            self.add_without_vertex(half_edge, twin_half_edge, edge)
            return
        if (edge[0] in self.vertices):
            self.init_half_edge_by_vertex(half_edge)
        if (edge[1] in self.vertices):
            self.init_half_edge_by_vertex(twin_half_edge)

        if (edge[0] not in self.vertices):
            origin_vertex = Vertex(edge[0], half_edge)
            self.vertices[edge[0]] = origin_vertex
        if (edge[1] not in self.vertices):
            end_vertex = Vertex(edge[1], twin_half_edge)
            self.vertices[edge[1]] = end_vertex
        self.half_edges.append(half_edge)
        self.half_edges.append(twin_half_edge)

    def add_without_vertex(self, half_edge, twin_half_edge, edge):

        origin_vertex = Vertex(edge[0], half_edge)
        end_vertex = Vertex(edge[1], twin_half_edge)

        half_edge.next = twin_half_edge
        half_edge.prev = twin_half_edge

        twin_half_edge.next = half_edge
        twin_half_edge.prev = half_edge

        self.vertices[edge[0]] = origin_vertex
        self.vertices[edge[1]] = end_vertex

        self.half_edges.append(half_edge)
        self.half_edges.append(twin_half_edge)

    def init_half_edge_by_vertex(self, half_edge: HalfEdge):

        start_half_edge = self.vertices[half_edge.origin].half_edge
        left_half_edge = start_half_edge
        right_half_edge = start_half_edge
        current_half_edge = start_half_edge.twin.next
        if (current_half_edge == current_half_edge.next):
            start_half_edge.prev = half_edge.twin
            half_edge.twin.next = start_half_edge

            start_half_edge.twin.next = half_edge
            half_edge.prev = start_half_edge.twin
            return

        half_edge_direction = half_edge.end - half_edge.origin

        while (current_half_edge != start_half_edge):

            current_half_edge_direction = current_half_edge.end - current_half_edge.origin

            is_left_half_angle_left_ccw = l_ccw_angle(
                half_edge_direction, left_half_edge.direction)
            is_right_half_angle_right_ccw = l_ccw_angle(
                right_half_edge.direction, half_edge_direction)

            if (is_left_half_angle_left_ccw):
                if (l_ccw_angle(half_edge_direction, current_half_edge_direction) and
                        l_ccw_angle(current_half_edge_direction, left_half_edge.direction)):
                    left_half_edge = current_half_edge
            elif (l_ccw_angle(half_edge_direction, current_half_edge_direction) or
                  l_ccw_angle(current_half_edge_direction, left_half_edge.direction)):
                left_half_edge = current_half_edge

            if (is_right_half_angle_right_ccw):
                if (l_ccw_angle(current_half_edge_direction, half_edge_direction) and
                        l_ccw_angle(right_half_edge.direction, current_half_edge_direction)):
                    right_half_edge = current_half_edge
            elif (l_ccw_angle(current_half_edge_direction, half_edge_direction) or
                  l_ccw_angle(left_half_edge.direction, current_half_edge_direction)):
                right_half_edge = current_half_edge

            current_half_edge = current_half_edge.twin.next

        right_half_edge.prev = half_edge.twin
        half_edge.twin.next = right_half_edge

        left_half_edge.twin.next = half_edge
        half_edge.prev = left_half_edge.twin
        if (half_edge.next == None):
            half_edge.next = half_edge.twin

    def init_faces(self):
        for half_edge in self.half_edges:
            if (half_edge.face != None):
                continue
            face = Face(half_edge)
            self.faces.append(face)
            half_edge.face = face
            current_edge = half_edge.next
            while (current_edge != half_edge):
                current_edge.face = face
                current_edge = current_edge.next

    def remove_degenerate_cases(self):
        for face in self.faces:
            if (not face.is_closed()):
                self.remove_unbounded_face(face)
                continue
            start_half_edge = face.boundary_half_edge
            if (start_half_edge.is_degenerate()):
                start_half_edge = self.remove_degenerate_half_edge(
                    start_half_edge)
            current_half_edge = start_half_edge.next
            while (current_half_edge != start_half_edge):
                if (current_half_edge.is_degenerate()):
                    current_half_edge = self.remove_degenerate_half_edge(
                        current_half_edge)
                current_half_edge = current_half_edge.next

    def remove_degenerate_half_edge(self, half_edge: HalfEdge) -> HalfEdge:
        next_half_edge = None
        if (half_edge.next == half_edge.twin):
            half_edge.prev.next = half_edge.twin.next
            half_edge.twin.next.prev = half_edge.prev
            next_half_edge = half_edge.twin.next
            self.vertices.pop(half_edge.end)
        else:
            half_edge.next.prev = half_edge.twin.prev
            half_edge.twin.prev.next = half_edge.next
            next_half_edge = half_edge.twin.prev
            self.vertices.pop(half_edge.origin)
        self.half_edges.remove(half_edge.twin)
        self.half_edges.remove(half_edge)
        if not next_half_edge.is_degenerate():
            return next_half_edge
        else:
            return self.remove_degenerate_half_edge(next_half_edge)

    def remove_unbounded_face(self, face: Face):
        start_half_edge = face.boundary_half_edge
        next_half_edge = start_half_edge.next
        prev_half_edge = start_half_edge.prev
        self.half_edges.remove(start_half_edge)

        while (next_half_edge != None):
            next_next_half_edge = next_half_edge.next
            self.half_edges.remove(next_half_edge)
            next_half_edge = next_next_half_edge
        while (prev_half_edge != None):
            prev_prev_half_edge = prev_half_edge.prev
            self.half_edges.remove(prev_half_edge)
            prev_half_edge = prev_prev_half_edge
        self.faces.remove(face)

    def get_outer_boundary(self):
        min_point = list(self.vertices.keys())[0]  # fix
        for point in self.vertices:
            if (point.y < min_point.y or point.y == min_point.y and point.x < min_point.x):
                min_point = point
        return self.vertices[point].half_edge.face.get()

    def get_optimal_point_in_area(self, width, height):
        optimal_point = Vector(width, height)
        for point in self.vertices:
            if (point.y >= 0 and point.y <= height and point.x >= 0 and point.x <= width and optimal_point > point):
                optimal_point = point
        return point


if __name__ == '__main__':
    dcel = DCEL([(Vector(0, 0), Vector(0, 1)), (Vector(0, 1), Vector(1, 1)), (Vector(
        1, 1), Vector(1, 0)), (Vector(1, 0), Vector(0, 0)), (Vector(0, 0), Vector(0.5, 0.5))])
    poly = dcel.faces[1].get()
    poly.draw()
    print()
