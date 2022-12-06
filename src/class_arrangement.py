from matplotlib import pyplot as plt
from class_direction import Direction, is_convex, psevdoProd
from class_segment import Segment
from class_vector import Vector
from shapely.geometry import LineString, Point


class Vertex:
    def __init__(self, point: Vector):
        self.point = point
        self.half_edges_by_ccw_angle: list[HalfEdge] = []
        self.label = None

    def add_half_edge(self, half_edge):
        for i in range(len(self.half_edges_by_ccw_angle)):
            if (self.half_edges_by_ccw_angle[i].direction > half_edge.direction):
                self.half_edges_by_ccw_angle.insert(i, half_edge)
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
        self.is_visited = False

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
        self.label = None
        self.is_hole = False
        self.is_visited = False

    def is_inside(self, point):
        # edges = []
        # if (self.boundary_half_edge == None):
        #     return True

        # def quadrant(v):
        #     return (1 if v.y >= 0 else 4) if v.x >= 0 else (
        #         2 if v.y >= 0 else 3)
        # half_edge = self.boundary_half_edge
        # edges.append(half_edge.original_edge)
        # a = half_edge.origin
        # if (point == a):
        #     return False
        # start_point = a
        # edges.append([point, a])
        # v = a-point
        # current_quadrant = quadrant(v)
        # half_edge = half_edge.next
        # edges.append(half_edge.original_edge)
        # a = half_edge.origin
        # if (point == a):
        #     return False
        # quadrants = 0
        # while (a != start_point):
        #     edges.append(half_edge.original_edge)
        #     prev_quadrant = current_quadrant
        #     a = half_edge.origin
        #     if (point == a):
        #         return False
        #     current_quadrant = quadrant(a-point)
        #     edges.append([point, a])
        #     if (prev_quadrant == 3 and current_quadrant == 0):
        #         quadrants += 1
        #     elif (current_quadrant > prev_quadrant):
        #         quadrants += 1
        #     elif (current_quadrant < prev_quadrant):
        #         quadrants -= 1
        #     half_edge = half_edge.next
        # if (quadrants == 4):
        #     print(True)
        # elif (quadrants == 0):
        #     print(False)
        # else:
        #     print('?')
        # draw_segments_sequence(edges)
        # if (quadrants > 0):
        #     return True
        # elif (quadrants == 0):
        #     return False
        # else:
        #     print('?')

        line = [point+Vector(0, 0.0001), Vector(point.x +
                                                100000, point.y+0.0001)]
        half_edge = self.boundary_half_edge
        if (not half_edge):
            return True
        segments = [[Vector(round(half_edge.origin.x, 6), round(half_edge.origin.y, 6)), Vector(
            round(half_edge.end.x, 6), round(half_edge.end.y, 6))]]
        current_half_edge = half_edge.next
        while (current_half_edge != half_edge):
            segments.append([Vector(round(current_half_edge.origin.x, 6), round(current_half_edge.origin.y, 6)), Vector(
                round(current_half_edge.end.x, 6), round(current_half_edge.end.y, 6))])
            current_half_edge = current_half_edge.next
        number_of_intersections = 0
        border_points = []
        for segment in segments:
            if (point == segment[0] or point == segment[1]):
                return False
            intersection = segment_intersection(line, segment)
            if (intersection):
                number_of_intersections += 1
        return True if number_of_intersections % 2 == 1 else False

        # half_edge = self.boundary_half_edge
        # current_half_edge = half_edge
        # if (not current_half_edge):
        #     return True
        # next_half_edge = half_edge.next

        # a = current_half_edge.origin
        # b = current_half_edge.end
        # c = next_half_edge.end
        # if (a == p or b == p or c == p):
        #     return False
        # ba = a-b
        # bc = c-b
        # bp = p - b
        # if (not isBetween(bp, bc, ba)):
        #     return False
        # current_half_edge = current_half_edge.next
        # next_half_edge = next_half_edge.next

        # while (current_half_edge != half_edge):
        #     a = current_half_edge.origin
        #     b = current_half_edge.end
        #     c = next_half_edge.end

        #     if (a == p or b == p or c == p):
        #         return False

        #     ba = a-b
        #     bc = c-b
        #     bp = p - b
        #     if (not isBetween(bp, bc, ba)):
        #         return False
        #     current_half_edge = current_half_edge.next
        #     next_half_edge = next_half_edge.next
        # return True

    def get_inside_point(self):
        current_half_edge = self.boundary_half_edge
        next_half_edge = current_half_edge.next

        a = current_half_edge.origin
        v = current_half_edge.end
        b = next_half_edge.end

        while (not is_convex(a, v, b)):  # find convex angle
            a = current_half_edge.origin
            v = current_half_edge.end
            b = next_half_edge.end
            current_half_edge = current_half_edge.next
            next_half_edge = next_half_edge.next

        min_distance = -1
        min_point = Vector(0, 0)
        next_half_edge = next_half_edge.next

        def is_inside(p):
            if (psevdoProd(p-a, v-a) >= 0 or psevdoProd(p-v, b-v) >= 0 or psevdoProd(p-b, a-b) >= 0):
                return False
            return True

        while (next_half_edge != current_half_edge):
            point = next_half_edge.end
            if (is_inside(point)):
                distance = point.x*v.x+point.y*v.y
                if (min_point.x == 0 and min_point.y == 0 or distance < min_distance):
                    min_distance = distance
                    min_point = point
            next_half_edge = next_half_edge.next
        return (a+b+v)*(0.3333333) if (min_point.x == 0 and min_point.y == 0) else (v+min_point)*0.5


class DCEL:
    def __init__(self) -> None:
        self.unbounded_face: Face = Face()
        self.faces: list[Face] = [self.unbounded_face]
        self.vertices: dict[Vector, Vertex] = dict()
        self.half_edges: list[HalfEdge] = []
        self.edges: list[tuple[Vector, Vector]] = []

    def add_edge(self, edge: tuple[Vector, Vector]):  # ПРОВЕРЕНО
        edge = [Vector(round(edge[0].x, 6), round(edge[0].y, 6)),
                Vector(round(edge[1].x, 6), round(edge[1].y, 6))]
        self.edges.append(edge)
        half_edge, twin_half_edge = HalfEdge.init_pair_halfedges(edge)

        is_origin_edge_incendent = edge[0] in self.vertices
        is_end_edge_incendent = edge[1] in self.vertices

        if (is_origin_edge_incendent, is_end_edge_incendent) == (False, False):  # NO_INCENDENT_VERTEX
            self.add_without_incendent_vertex(half_edge, twin_half_edge)

        if (is_origin_edge_incendent, is_end_edge_incendent) == (True, False):  # ONLY_ORIGIN_VERTEX_INCENDENT
            self.add_half_edge_with_incendent_vertex(half_edge)
            end_vertex = Vertex(edge[1])
            end_vertex.add_half_edge(twin_half_edge)
            self.vertices[edge[1]] = end_vertex

        if (is_origin_edge_incendent, is_end_edge_incendent) == (False, True):  # ONLY_END_VERTEX_INCENDENT
            self.add_half_edge_with_incendent_vertex(twin_half_edge)
            origin_vertex = Vertex(edge[0])
            origin_vertex.add_half_edge(half_edge)
            self.vertices[edge[0]] = origin_vertex

        if (is_origin_edge_incendent, is_end_edge_incendent) == (True, True):  # BOTH_VERTEX_INCENDENT
            origin_vertex = self.vertices[half_edge.origin]
            for incindent_half_edge in origin_vertex.half_edges_by_ccw_angle:
                if (incindent_half_edge.end == half_edge.end):
                    self.edges.pop()
                    return
            self.add_half_edge_with_incendent_vertex(half_edge)
            self.add_half_edge_with_incendent_vertex(twin_half_edge)

        self.half_edges.append(half_edge)
        self.half_edges.append(twin_half_edge)

    def add_without_incendent_vertex(self, half_edge: HalfEdge, twin_half_edge: HalfEdge):
        origin_vertex = Vertex(half_edge.origin)
        origin_vertex.add_half_edge(half_edge)

        end_vertex = Vertex(twin_half_edge.origin)
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
            half_edge.twin.prev = half_edge

    def init_faces(self):  # change
        for half_edge in self.half_edges:
            if (half_edge.is_visited):
                continue
            start_half_edge = half_edge
            start_half_edge.is_visited = True

            current_half_edge = half_edge.next
            if (current_half_edge.is_visited):
                continue
            current_half_edge.is_visited = True

            while (half_edge != current_half_edge):
                if (start_half_edge.origin > current_half_edge.origin):
                    start_half_edge = current_half_edge
                current_half_edge = current_half_edge.next
                if (current_half_edge.is_visited):
                    continue
                current_half_edge.is_visited = True
            if (psevdoProd(start_half_edge.origin - start_half_edge.prev.origin, start_half_edge.end - start_half_edge.prev.origin) < 0):  # check orientation
                continue

            new_face = Face()
            new_face.boundary_half_edge = start_half_edge
            start_half_edge.face = new_face
            start_half_edge.is_visited = True

            current_half_edge = start_half_edge.next
            current_half_edge.face = new_face
            current_half_edge.is_visited = True

            while (current_half_edge != start_half_edge):
                current_half_edge.is_visited = True
                current_half_edge = current_half_edge.next
                current_half_edge.face = new_face
            self.faces.append(new_face)

        self.init_holes()
        # for face in self.faces:
        #     boundary_half_edge = face.boundary_half_edge
        #     if (boundary_half_edge == None):
        #         face.is_hole = True
        #         continue
        #     hole_order = 0
        #     while (boundary_half_edge != None):
        #         hole_order += 1
        #         boundary_half_edge = boundary_half_edge.twin.face.boundary_half_edge
        #     face.is_hole = False if hole_order % 2 == 1 else False
        self.painting_faces(self.unbounded_face, False)

    def init_holes(self):  # change
        for half_edge in self.half_edges:
            half_edge.is_visited = False

        for half_edge in self.half_edges:
            if (half_edge.face != None or half_edge.is_visited):
                continue

            face = self.get_face_by_inside_point(half_edge.origin)
            face.holes_half_edges.append(half_edge)
            half_edge.face = face
            half_edge.is_visited = True
            half_edge.next.is_visited = True
            half_edge.next.face = face
            current_half_edge = half_edge.next
            while (current_half_edge != half_edge):
                current_half_edge = current_half_edge.next
                current_half_edge.is_visited = True
                current_half_edge.face = face

    def painting_faces(self, face: Face, outer_face_is_hole: bool):
        face.is_hole = not outer_face_is_hole
        outer_face_is_hole = not outer_face_is_hole
        face.is_visited = True

        for hole_half_edge in face.holes_half_edges:
            if (not hole_half_edge.twin.face.is_visited):
                self.painting_faces(
                    hole_half_edge.twin.face, outer_face_is_hole)
            current_hole_half_edge = hole_half_edge.next
            while (current_hole_half_edge != hole_half_edge):
                if (not current_hole_half_edge.twin.face.is_visited):
                    self.painting_faces(
                        current_hole_half_edge.twin.face, outer_face_is_hole)
                current_hole_half_edge = current_hole_half_edge.next

    def get_face_by_inside_point(self, point: Vector):
        face = self.unbounded_face
        for current_face in self.faces:
            if (current_face.boundary_half_edge is None):
                continue
            if (current_face.is_inside(point) and face.is_inside(current_face.boundary_half_edge.origin)):
                face = current_face
        return face

    @staticmethod
    def subdivision(d1, d2):

        edges = []
        for edge in d1.edges:
            edges.append(edge)
        for edge in d2.edges:
            edges.append(edge)
        edges = Segment.split_by_intersections(edges)
        subdiv = DCEL()
        for edge in edges:
            subdiv.add_edge(edge)
        subdiv.init_faces()
        for face in subdiv.faces:
            if (face.boundary_half_edge == None):
                continue
            inside_point = face.get_inside_point()
            is_inside_fist_face = not d1.get_face_by_inside_point(
                inside_point).is_hole
            is_inside_second_face = not d2.get_face_by_inside_point(
                inside_point).is_hole
            if (is_inside_fist_face and is_inside_second_face):
                face.label = 'AB'
            elif (not is_inside_fist_face and is_inside_second_face):
                face.label = 'B'
            elif (is_inside_fist_face and not is_inside_second_face):
                face.label = 'A'
        return subdiv

    @staticmethod
    def logical_and(d1, d2):
        subdiv = DCEL.subdivision(d1, d2)

        log_and = DCEL()
        for face in subdiv.faces:
            if (face.label != 'AB'):
                continue
            half_edge = face.boundary_half_edge
            current_half_edge = half_edge.next
            log_and.add_edge(half_edge.original_edge)
            while (half_edge != current_half_edge):
                log_and.add_edge(current_half_edge.original_edge)
                current_half_edge = current_half_edge.next
        log_and.init_faces()
        return log_and

    @staticmethod
    def logical_or(d1, d2):
        subdiv = DCEL.subdivision(d1, d2)
        # subdiv.draw()
        log_or = DCEL()
        # for face in subdiv.faces:
        #     if (face.label == 'AB' or face.label == None):
        #         continue
        #     half_edge = face.boundary_half_edge
        #     current_half_edge = half_edge.next
        #     if (half_edge.twin.face.label != 'AB'):
        #         log_or.add_edge(half_edge.original_edge)
        #     while (half_edge != current_half_edge):
        #         if (current_half_edge.twin.face.label != 'AB'):
        #             log_or.add_edge(current_half_edge.original_edge)
        #         current_half_edge = current_half_edge.next
        # for face in subdiv.faces:
        #     if (face.label != 'AB'):
        #         continue
        #     half_edge = face.boundary_half_edge
        #     current_half_edge = half_edge.next
        #     if (half_edge.twin.face.label == None):
        #         log_or.add_edge(half_edge.original_edge)
        #     while (half_edge != current_half_edge):
        #         if (current_half_edge.twin.face.label == None):
        #             log_or.add_edge(current_half_edge.original_edge)
        #         current_half_edge = current_half_edge.next
        for half_edge in subdiv.half_edges:
            if (half_edge.face.label == 'AB' and half_edge.twin.face.label != None or half_edge.twin.face.label == 'AB' and half_edge.face.label != None):
                continue
            log_or.add_edge(half_edge.original_edge)
        log_or.init_faces()
        return log_or

    def logical_minus(d1, d2):
        subdiv = DCEL.subdivision(d1, d2)
        log_minus = DCEL()
        for face in subdiv.faces:
            if (face.label != 'A'):
                continue
            half_edge = face.boundary_half_edge
            current_half_edge = half_edge.next
            log_minus.add_edge(half_edge.original_edge)
            while (half_edge != current_half_edge):
                log_minus.add_edge(current_half_edge.original_edge)
                current_half_edge = current_half_edge.next
        log_minus.init_faces()
        return log_minus

    def draw(self):
        segments = []
        for face in self.faces:
            start_half_edge = face.boundary_half_edge
            if (start_half_edge is None):
                continue
            segments.append((start_half_edge.origin, start_half_edge.end))
            current_half_edge = start_half_edge.next
            while (start_half_edge != current_half_edge):
                segments.append(
                    (current_half_edge.origin, current_half_edge.end))
                current_half_edge = current_half_edge.next
        for segment in segments:
            plt.arrow(segment[0].x, segment[0].y, segment[1].x-segment[0].x, segment[1].y-segment[0].y,
                      shape='full', lw=0.5, length_includes_head=True, head_width=.05)
        plt.show()


def segment_intersection(segment1, segment2):
    A = (segment1[0].x, segment1[0].y)
    B = (segment1[1].x, segment1[1].y)

    C = (segment2[0].x, segment2[0].y)
    D = (segment2[1].x, segment2[1].y)

    line_1 = LineString([A, B])
    line_2 = LineString([C, D])
    int_pt = line_1.intersection(line_2)
    if type(int_pt) == Point:
        return [Vector(float(int_pt.x), float(int_pt.y))]
    elif type(int_pt) == LineString:
        if (len(int_pt.bounds) == 0):
            return []
        return [Vector(float(int_pt.bounds[0]), float(int_pt.bounds[1])), Vector(float(int_pt.bounds[2]), float(int_pt.bounds[3]))]


def draw_segments_sequence(segments):
    for segment in segments:
        plt.arrow(segment[0].x, segment[0].y, segment[1].x-segment[0].x, segment[1].y-segment[0].y,
                  shape='full', lw=0.5, length_includes_head=True, head_width=.05)
    plt.show()


if __name__ == '__main__':

    segments1 = [[Vector(0, 0), Vector(1, 0)], [Vector(1, 0), Vector(1, 1)], [
        Vector(1, 1), Vector(0, 1)], [Vector(0, 1), Vector(0, 0)]]
    segments2 = [[Vector(0.5, 0), Vector(1.5, 0)], [Vector(1.5, 0), Vector(1.5, 1)], [
        Vector(1.5, 1), Vector(0.5, 1)], [Vector(0.5, 1), Vector(1.5, 0)]]
    dcel1 = DCEL()
    dcel2 = DCEL()

    for seg in segments1:
        dcel1.add_edge(seg)
    for seg in segments2:
        dcel2.add_edge(seg)
    dcel2.init_faces()
    dcel1.init_faces()
    #log_and = DCEL.logical_and(dcel1, dcel2)
    # log_and.draw()
    log_or = DCEL.logical_or(dcel1, dcel2)
   # log_or.draw()
    log_min = DCEL.logical_minus(dcel1, dcel2)
    # log_min.draw()
    print()
