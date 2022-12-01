
from copy import deepcopy
from class_direction import Direction
from class_segment import Segment
from class_vector import Vector


class Vertex:  # OK
    def __init__(self, point: Vector):
        self.point = point
        self.half_edges_by_ccw_angle: list[HalfEdge] = []

    def add_half_edge(self, half_edge):
        for i in range(len(self.half_edges_by_ccw_angle)):
            if (self.half_edges_by_ccw_angle[i].direction > half_edge.direction):
                self.half_edges_by_ccw_angle.insert(i, half_edge)
                return
        self.half_edges_by_ccw_angle.append(half_edge)


class HalfEdge:  # OK

    def __init__(self):
        self.original_edge: tuple[Vector, Vector] = None
        self.origin: Vector = None
        self.end: Vector = None
        self.twin: HalfEdge = None
        self.prev: HalfEdge = None
        self.next: HalfEdge = None
        self.face: Face = None
        self.vertex: Vertex = None
        self.direction: Direction = None

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


class Face:  # OK
    def __init__(self, half_edge=None):
        self.boundary_half_edge: HalfEdge = half_edge
        self.holes_half_edges: list[HalfEdge] = []
        self.label = None


class DCEL:
    def __init__(self, edges: list[tuple[Vector, Vector]] = [], without_intersection=False) -> None:
        self.unbounded_face: Face = None
        self.faces: list[Face] = []
        self.vertices: dict[Vector, Vertex] = dict()
        self.half_edges: list[HalfEdge] = []
        self.edges: list[tuple[tuple[Vector, Vector], HalfEdge, HalfEdge]] = []
        self.build_dcel(edges)

    def build_dcel(self, edges):  # NOT OK
        def handle_event(event, event_type):
            self.add_edge(event.segment)
        sweep_line(edges, handle_event)

    def add_edge(self, edge: tuple[Vector, Vector]):  # ПРОВЕРЕНО
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

    @staticmethod
    def subdivision(d1: 'DCEL', d2: 'DCEL') -> 'DCEL':  # NOT OK
        subdiv = DCEL()
        subdiv.half_edges = deepcopy(d1.half_edges+d2.half_edges)
        subdiv.vertices = deepcopy(d1.vertices | d2.vertices)

        def handle_event(event, event_type):
            if (event_type == 1):  # Left Point
                subdiv.vertices[event.point] = event.segments[0].half_edge.vertex
                if ()

            if (event_type == 2):  # Right Point
                pass
            if (event_type == 3):  # Intersection
                pass

    @staticmethod
    def set_and(d1, d2):  # NEED TEST
        subdiv = DCEL.subdivision(d1, d2)

        def is_belong(edge_with_half_edges):
            return (edge_with_half_edges[1].face.label == 'AB' or
                    edge_with_half_edges[2].face.label == 'AB')

        belonging_edges_with_half_edges = filter(is_belong, subdiv.edges)

        belonging_edges = list(
            map(lambda x: x[0], belonging_edges_with_half_edges))

        set_and = DCEL(belonging_edges, without_intersection=True)
        return set_and

    @ staticmethod
    def set_or(d1, d2):  # NEED TEST
        subdiv = DCEL.subdivision(d1, d2)

        def is_belong(edge):
            return ((edge[1].face.label in ('A', 'B') and edge[2].face.label != 'AB') or
                    (edge[2].face.label in ('A', 'B') and edge[1].face.label != 'AB') or
                    (edge[1].face.label == 'AB' and edge[2].face.label == None) or
                    (edge[2].face.label == 'AB' and edge[1].face.label == None))

        belonging_edges_with_half_edges = filter(is_belong, subdiv.edges)

        belonging_edges = list(
            map(lambda x: x[0], belonging_edges_with_half_edges))

        set_or = DCEL(belonging_edges, without_intersection=True)
        return set_or

    @ staticmethod
    def logical_minus(d1, d2):  # NEED TEST
        subdiv = DCEL.subdivision(d1, d2)

        def is_belong(edge_with_half_edges):
            return edge_with_half_edges[1].face.label == 'A' or edge_with_half_edges[2].face.label == 'A'

        belonging_edges_with_half_edges = filter(is_belong, subdiv.edges)

        belonging_edges = list(
            map(lambda x: x[0], belonging_edges_with_half_edges))

        set_minus = DCEL(belonging_edges, without_intersection=True)
        return set_minus
