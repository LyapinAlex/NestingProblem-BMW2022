from copy import deepcopy
import copy
import math
from matplotlib import pyplot as plt

import numpy as np
from class_Dcel_sweep_line import Event, EventQueue, Status, StatusNode, StatusValue, SweepLine
from class_cycle_graph import Graph
from class_direction import Direction, is_convex, psevdoProd
from class_segment import Segment
from class_vector import Vector
from memory_structure.class_AVL_tree import AvlTree, Node

####Добавление новой функциональности к Sweep Line#####


class DcelEventValue:  # OK
    def __init__(self) -> None:
        self.upper_segments = set()
        self.inner_segments = set()
        self.lower_segments = set()
        self.vertex: Vertex = None


class DcelEvent(Event):
    def __init__(self, point, value=None):
        if (value is None):
            value = DcelEventValue()
        super().__init__(point, value)


class DcelEventQeue(EventQueue):
    def __init__(self):
        super().__init__()

    def create_node(self, key):
        return DcelEvent(key)


class DcelStatusValue(StatusValue):
    def __init__(self) -> None:
        super().__init__()
        self.half_edge: HalfEdge = None
        self.twin_half_edge: HalfEdge = None
        self.incindent_vertex: Vertex = None
        self.original_incendent_face = None


class DcelStatusNode(StatusNode):
    def __init__(self, key, original_incendent_face=None, value=None):
        if (value is None):
            value = DcelStatusValue()
        super().__init__(key, value)
        self.init_half_edges(key)
        if (original_incendent_face is not None):
            self.value.original_incendent_face = original_incendent_face

    def init_half_edges(self, key):
        half_edge, twin_half_edge = HalfEdge.init_pair_halfedges(key)
        self.value.half_edge = half_edge
        self.value.twin_half_edge = twin_half_edge


class DcelStatus(Status):
    def __init__(self):
        super().__init__()

    def create_node(self, key):
        node = DcelStatusNode(key)
        node.value.status = self
        return node


"""Обработчки событий, который для каждого события создает новый Vertex, добавляет к нему
    нужные HalfEdges, сплитит их, кроме того добавляет в Vertex ссылку на HalfEdge который лежит
    непосредственно слева от Vertex"""


class BuildHandler:
    def __init__(self, dcel: 'DCEL') -> None:
        self.dcel = dcel

    def handle_upper(self, event, event_qeue, status):
        vertex = event.value.vertex

        for segment in event.value.upper_segments:
            found_status = status.find(segment)
            self.dcel.half_edges.append(found_status.value.half_edge)
            vertex.add_half_edge(self.dcel.half_edges[-1])

    def handle_vertex(self, event):
        vertex = Vertex(event.key)
        event.value.vertex = vertex
        self.dcel.vertices.insert(vertex)

    def handle_inner(self, event, event_qeue, status):
        vertex = event.value.vertex

        for segment in event.value.inner_segments:
            found_status = status.find(segment)
            # Не уверен, что нужно копировать, но на всякий случай
            prev_end = copy.copy(found_status.key.min_point)

            found_status.value.half_edge.end = event.key
            found_status.value.twin_half_edge.origin = event.key

            self.dcel.half_edges.append(found_status.value.twin_half_edge)
            vertex.add_half_edge(self.dcel.half_edges[-1])

            half_edge, twin_half_edge = HalfEdge.init_pair_halfedges(
                Segment(event.key, prev_end))
            self.dcel.half_edges.append(half_edge)

            vertex.add_half_edge(self.dcel.half_edges[-1])

            found_status.value.half_edge = half_edge
            found_status.value.twin_half_edge = twin_half_edge

    def handle_lower(self, event, event_qeue, status):
        vertex = event.value.vertex
        rightmost = None
        for segment in event.value.lower_segments:
            found_status = status.find(segment)
            if (rightmost is None or rightmost < found_status):
                rightmost = found_status
            self.dcel.half_edges.append(found_status.value.twin_half_edge)
            vertex.add_half_edge(self.dcel.half_edges[-1])

        for segment in event.value.inner_segments:
            found_status = status.find(segment)
            if (rightmost is None or rightmost < found_status):
                rightmost = found_status

        right_neighbour = None
        if (rightmost is not None):
            right_neighbour, _ = status.get_nearests(rightmost.key)

        if right_neighbour is not None:
            if (right_neighbour.key.compare_with_point(vertex.key) == 1):
                vertex.right_half_edge = right_neighbour.value.half_edge
            else:
                vertex.right_half_edge = right_neighbour.value.twin_half_edge


class DcelBuilder(SweepLine):
    def __init__(self, segments: list[Segment], handler=None) -> None:
        status = DcelStatus()
        event_qeue = DcelEventQeue()
        super().__init__(segments, status, event_qeue, handler)
#######################################################


class VertexValue:
    def __init__(self, point) -> None:
        self.key = point
        self.half_edges_by_ccw_angle: list[HalfEdge] = []
        self.right_half_edge: HalfEdge = None


class Vertex(Node):
    def __init__(self, key, value=Node):
        value = VertexValue(key)
        super().__init__(key, value)

    def add_half_edge(self, half_edge):
        is_append = False
        for i in range(len(self.value.half_edges_by_ccw_angle)):
            if (self.value.half_edges_by_ccw_angle[i].direction > half_edge.direction):
                self.value.half_edges_by_ccw_angle.insert(i, half_edge)
                is_append = True
                break
        if not is_append:
            self.value.half_edges_by_ccw_angle.append(half_edge)
        half_edge_index = self.value.half_edges_by_ccw_angle.index(
            half_edge)

        size = len(self.value.half_edges_by_ccw_angle)

        left_half_edge = self.value.half_edges_by_ccw_angle[(  # by ccw angle
            half_edge_index+1) % size]
        right_half_edge = self.value.half_edges_by_ccw_angle[(  # by ccw angle
            half_edge_index-1) % size]

        right_half_edge.prev = half_edge.twin
        half_edge.twin.next = right_half_edge

        left_half_edge.twin.next = half_edge
        half_edge.prev = left_half_edge.twin

        if (half_edge.next == None):
            half_edge.next = half_edge.twin
            half_edge.twin.prev = half_edge
        half_edge.vertex = self


class Verticies(AvlTree):
    def __init__(self):
        super().__init__()

    def create_node(self, key):
        node = Vertex(key)
        return node


class HalfEdge:  # OK

    def __init__(self):
        self.original_edge: Segment = None
        self.origin: Vector = None
        self.end: Vector = None
        self.twin: HalfEdge = None
        self.prev: HalfEdge = None
        self.next: HalfEdge = None
        self.face: Face = None
        self.vertex: Vertex = None
        self.direction: Direction = None
        self.is_visited = False
        self.cycle_node = None

    @staticmethod
    def init_pair_halfedges(edge: Segment):

        half_edge = HalfEdge()
        twin_half_edge = HalfEdge()

        half_edge.original_edge = edge
        twin_half_edge.original_edge = edge

        half_edge.twin = twin_half_edge
        twin_half_edge.twin = half_edge

        half_edge.origin = edge.max_point
        half_edge.end = edge.min_point

        twin_half_edge.origin = edge.min_point
        twin_half_edge.end = edge.max_point

        half_edge.direction = Direction(edge.min_point-edge.max_point)
        twin_half_edge.direction = Direction(edge.max_point-edge.min_point)

        return half_edge, twin_half_edge


class Face:  # OK
    def __init__(self, half_edge=None):
        self.boundary_half_edge: HalfEdge = half_edge
        self.holes_half_edges: list[HalfEdge] = []
        self.label = None
        self.is_hole = False
        self.is_visited = False

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

        def is_inside(p):
            if (psevdoProd(p-a, v-a) > 0 or psevdoProd(p-v, b-v) > 0 or psevdoProd(p-b, a-b) > 0):
                return False
            return True

        next_half_edge = next_half_edge.next

        while (next_half_edge != current_half_edge):
            point = next_half_edge.end
            if (is_inside(point)):
                distance = point.x*v.x+point.y*v.y
                if (min_point.x == 0 and min_point.y == 0 or distance < min_distance):
                    min_distance = distance
                    min_point = point
            next_half_edge = next_half_edge.next
        return (a+b+v)*(1/3) if (min_point.x == 0 and min_point.y == 0) else (v+min_point)*(1/2)

    def init_hole(self, prev_face):
        self.is_visited = True
        if (prev_face is None):
            self.is_hole = True
        else:
            self.is_hole = not prev_face.is_hole
        for hole_half_edge in self.holes_half_edges:
            start_half_edge = hole_half_edge
            start_half_edge.face = self
            if (start_half_edge.twin.face is not None and not start_half_edge.twin.face.is_visited):
                start_half_edge.twin.face.is_visited = True
                start_half_edge.twin.face.init_hole(self)
            current_half_edge = hole_half_edge.next
            while (current_half_edge != start_half_edge):
                current_half_edge.face = self
                if (current_half_edge.twin.face is not None and not current_half_edge.twin.face.is_visited):
                    current_half_edge.twin.face.is_visited = True
                    current_half_edge.twin.face.init_hole(self)
                current_half_edge = current_half_edge.next

    def is_inside(self, point: Vector):
        if (self.boundary_half_edge is None):
            return True

        start_half_edge = self.boundary_half_edge
        current_half_edge = start_half_edge.next
        v = start_half_edge.end - start_half_edge.origin
        angle = 0

        a = start_half_edge.origin
        b = start_half_edge.end

        pa = a-point
        pb = b-point

        if (pa.x**2+pa.y**2 < 0.000000001 or pb.x**2+pb.y**2 < 0.000000001):
            return True

        orient = psevdoProd(b-point, a-point)
        cos = (pa.x*pb.x+pa.y*pb.y) / \
            (math.sqrt(pa.x**2+pa.y**2)*math.sqrt(pb.x**2+pb.y**2))
        if (cos > 1):
            cos = 1
        if (cos < -1):
            cos = -1

        if (orient > 0):
            angle += math.acos(cos)
        elif (orient < 0):
            angle -= math.acos(cos)

        while (current_half_edge != start_half_edge):
            a = current_half_edge.origin
            b = current_half_edge.end

            pa = a-point
            pb = b-point

            if (pa.x**2+pa.y**2 < 0.000000001 or pb.x**2+pb.y**2 < 0.000000001):
                return True
            v = current_half_edge.end - current_half_edge.origin
            orient = psevdoProd(b - point, a-point)
            cos = (pa.x*pb.x+pa.y*pb.y) / \
                (math.sqrt(pa.x**2+pa.y**2)*math.sqrt(pb.x**2+pb.y**2))
            if (cos > 1):
                cos = 1
            if (cos < -1):
                cos = -1
            if (orient > 0):
                angle += math.acos(cos)
            elif (orient < 0):
                angle -= math.acos(cos)
            current_half_edge = current_half_edge.next

        if (abs(angle) > 0.00001):
            return True
        return False


class DCEL:
    def __init__(self, edges: list[tuple[Vector, Vector]] = []) -> None:
        self.unbounded_face: Face = Face()
        self.faces: list[Face] = [self.unbounded_face]
        self.vertices: Verticies = Verticies()
        self.half_edges: list[HalfEdge] = []
        if (len(edges) != 0):
            self.build_dcel(edges)

    def build_dcel(self, edges):
        # Начальная инициализация
        status = DcelStatus()
        event_qeue = EventQueue()
        handler = BuildHandler(self)
        sweep_line = DcelBuilder(edges, handler)
        self.init_faces()
        self.init_holes()

    def init_faces(self):  # change
        cycle_graph = Graph()
        unbounded_node = cycle_graph.create_node()
        unbounded_node.is_hole = False
        for half_edge in self.half_edges:
            if (half_edge.is_visited):
                continue
            half_edge.is_visited = True
            node = cycle_graph.create_node()
            node.half_edge = half_edge
            half_edge.cycle_node = node
            current_half_edge = half_edge.next
            while (current_half_edge != half_edge):
                current_half_edge.is_visited = True
                current_half_edge.cycle_node = node
                current_half_edge = current_half_edge.next

        for half_edge in self.half_edges:
            half_edge.is_visited = False

        for half_edge in self.half_edges:
            if (half_edge.is_visited):
                continue
            half_edge.is_visited = True
            start_half_edge = half_edge
            rightmost_half_edge = half_edge
            rightmost_vertex = half_edge.vertex
            current_half_edge = half_edge.next

            half_edge_whose_next_is_not_twin = half_edge if half_edge.next != half_edge.twin else False
            is_closed = half_edge.twin != half_edge.next
            while (current_half_edge != start_half_edge):
                if (half_edge_whose_next_is_not_twin is None):
                    half_edge_whose_next_is_not_twin = current_half_edge if current_half_edge.next != current_half_edge.twin else None
                elif is_closed:
                    is_closed = current_half_edge.twin != half_edge_whose_next_is_not_twin
                if (rightmost_vertex.key.x <= current_half_edge.vertex.key.x):
                    rightmost_vertex = current_half_edge.vertex
                    rightmost_half_edge = current_half_edge
                current_half_edge.is_visited = True
                current_half_edge = current_half_edge.next
            connected_half_edge = rightmost_vertex.value.right_half_edge
            connected_node = None
            if (connected_half_edge is not None):
                connected_node = connected_half_edge.node

            is_hole = not is_closed
            if (is_closed):
                orient = 1  # <0 если по часовой, >0 если против часовой
                half_edge_for_orient = rightmost_half_edge.prev
                while (half_edge_for_orient.prev == half_edge_for_orient.twin):
                    if (half_edge_for_orient == rightmost_half_edge):
                        orient = 0
                        break
                    half_edge_for_orient = half_edge_for_orient.prev
                is_hole = False
                if (orient != 0):
                    is_hole = psevdoProd(
                        rightmost_half_edge.origin - half_edge_for_orient.origin, rightmost_half_edge.end - half_edge_for_orient.origin) < 0
                else:
                    is_hole = True
            rightmost_half_edge.cycle_node.is_hole = is_hole
            if (is_hole and connected_node is None):
                cycle_graph.connect_nodes(
                    rightmost_half_edge.cycle_node, unbounded_node)
            if (connected_node is not None and not is_hole):
                cycle_graph.connect_nodes(
                    rightmost_half_edge.cycle_node, connected_node)

        for node in cycle_graph.nodes:
            if node.is_hole:
                continue
            if (node.half_edge is None):
                self.unbounded_face.holes_half_edges = list(
                    map(lambda elem: elem.half_edge, cycle_graph.get_all_neighbours(node)))
                continue
            face = Face()
            face.boundary_half_edge = node.half_edge
            node.half_edge.face = face
            face.holes_half_edges = list(
                map(lambda elem: elem.half_edge, cycle_graph.get_all_neighbours(node)))

            self.faces.append(face)

        for half_edge in self.half_edges:
            half_edge.face = half_edge.cycle_node.half_edge.face
            half_edge.is_visited = False

    def init_holes(self):
        self.unbounded_face.init_hole(prev_face=None)

    def get_face_by_inside_point(self, point: Vector):
        face = self.unbounded_face
        for current_face in self.faces:
            if (current_face.boundary_half_edge is None):
                continue
            if (current_face.is_inside(point) and face.is_inside(current_face.boundary_half_edge.origin)):
                face = current_face
        return face

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

    @staticmethod
    # TODO: Сделать через sweep line нормально
    def subdivision(d1: 'DCEL', d2: 'DCEL') -> 'DCEL':
        edges = []
        for half_edge in d1.half_edges:
            if (half_edge.is_visited):
                continue
            half_edge.is_visited = True
            half_edge.twin.is_visited = True
            segment = Segment(half_edge.origin, half_edge.end)
            edges.append(segment)

        for half_edge in d2.half_edges:
            if (half_edge.is_visited):
                continue
            half_edge.is_visited = True
            half_edge.twin.is_visited = True
            segment = Segment(half_edge.origin, half_edge.end)
            edges.append(segment)

        subdiv = DCEL(edges)

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
    def set_and(d1, d2):  # NEED TEST
        subdiv = DCEL.subdivision(d1, d2)

        def is_belong(half_edge):
            return (half_edge.face.label == 'AB' and half_edge.twin.face.label != 'AB')

        belonging_half_edges = filter(is_belong, subdiv.half_edges)
        belonging_edges = list(
            map(lambda x: Segment(x.origin, x.end), belonging_half_edges))

        set_and = DCEL(belonging_edges)
        return set_and

    @ staticmethod
    def set_or(d1, d2):  # NEED TEST
        subdiv = DCEL.subdivision(d1, d2)

        def is_belong(half_edge):
            return ((half_edge.face.label in ('A', 'B') and half_edge.twin.face.label != 'AB') or
                    (half_edge.face.label == 'AB' and half_edge.twin.face.label == None))

        belonging_half_edges = filter(is_belong, subdiv.half_edges)

        belonging_edges = list(
            map(lambda x: Segment(x.origin, x.end), belonging_half_edges))

        set_or = DCEL(belonging_edges)
        return set_or

    @ staticmethod
    def set_minus(d1, d2):  # NEED TEST
        subdiv = DCEL.subdivision(d1, d2)

        def is_belong(half_edge):
            return half_edge.face.label == 'A'

        belonging_half_edges = filter(is_belong, subdiv.half_edges)

        belonging_edges = list(
            map(lambda x: Segment(x.origin, x.end), belonging_half_edges))

        set_minus = DCEL(belonging_edges)
        return set_minus


def rundom_segments(num_segments=10) -> list[Segment]:
    random_float_array = np.random.uniform(
        0, 100, size=(num_segments * 4))
    A = Vector(0, 50)
    B = Vector(20, 50)
    C = Vector(40, 50)
    D = Vector(60, 50)
    E = Vector(80, 50)
    F = Vector(100, 50)
    s1 = Segment(A, B)
    s2 = Segment(B, C)
    s3 = Segment(C, D)
    s4 = Segment(A, F)
    array_segments = []
    for i in range(num_segments):
        p1 = Vector(
            float(random_float_array[4*i]), float(random_float_array[4*i+1])).round()
        p2 = Vector(float(random_float_array[4*i+2]),
                    float(random_float_array[4*i+3])).round()
        array_segments.append(Segment(p1, p2))
    return array_segments


def draw_segments_sequence(segments):
    for segment in segments:
        plt.arrow(segment[0].x, segment[0].y, segment[1].x-segment[0].x, segment[1].y-segment[0].y,
                  shape='full', lw=0.5, length_includes_head=True, head_width=.05)
    plt.show()


def draw_lines(array_segments: list[Segment], intersection_points: list, current_segments=None, left_neighbour=None, right_neighbour=None):
    fig, ax = plt.subplots()
    if intersection_points:
        x_values = []
        y_values = []
        for point in intersection_points:
            x_values.append(point.x)
            y_values.append(point.y)
        ax.scatter(x_values, y_values, c='red', marker='o')
    for segment in array_segments:
        p1 = segment.min_point
        p2 = segment.max_point
        x_values = [p1.x, p2.x]
        y_values = [p1.y, p2.y]
        plt.plot(x_values, y_values, 'b', linestyle="-")
    if (current_segments):
        for segment in current_segments:
            p1 = segment.min_point
            p2 = segment.max_point
            x_values = [p1.x, p2.x]
            y_values = [p1.y, p2.y]
            plt.plot(x_values, y_values, 'r', linestyle="-")
    if (left_neighbour):
        p1 = left_neighbour.min_point
        p2 = left_neighbour.max_point
        x_values = [p1.x, p2.x]
        y_values = [p1.y, p2.y]
        plt.plot(x_values, y_values, 'g', linestyle="-")
    if (right_neighbour):
        p1 = right_neighbour.min_point
        p2 = right_neighbour.max_point
        x_values = [p1.x, p2.x]
        y_values = [p1.y, p2.y]
        plt.plot(x_values, y_values, 'g', linestyle="-")
    plt.show()
    return


def main():
    array_segments = rundom_segments(10)

    other_array_segments = rundom_segments(10)
    dcel1 = DCEL(array_segments)
    dcel2 = DCEL(other_array_segments)
    set_or = DCEL.set_and(dcel1, dcel2)
    print('some')
    # sweep_line = SweepLine(array_segments, Status(), EventQueue())
    # sweep_line.event_queue.inorder_print()
    # print(len(sweep_line.intersection_points))
    # draw_lines(array_segments, sweep_line.intersection_points)


if __name__ == '__main__':
    main()
    # ТЕСТЫ
    # a0 = Vector(0, 0)
    # b0 = Vector(1, 0)
    # c0 = Vector(2, 0)
    # a1 = Vector(0, 1)
    # b1 = Vector(1, 1)
    # c1 = Vector(2, 1)
    # s1 = Segment(a0, c1)
    # s2 = Segment(b0, b1)
    # s3 = Segment(c0, a1)
    # s1 = Segment(Vector(0, 0), Vector(1, 1))
    # s2 = Segment(Vector(0, -1), Vector(1, 0))
    # s3 = Segment(Vector(0.7, -2), Vector(0.3, 1))
    # s4 = Segment(Vector(0, -3), Vector(1, 2.5))

    # segments = [s1, s2, s3]
    # v1 = Vector(1, 1)
    # v0 = 0*v1
    # v2 = 2*v1
    # v3 = 3*v1
    # w1 = Segment(v0, v2)
    # w2 = Segment(v0, b0)
    # segments = [w1, w2]

    # m0 = Vector(0, 1)
    # m1 = Vector(1, 0)
    # p0 = Vector(2, 1)
    # p1 = Vector(1, 2)
    # t1 = Segment(m0, p0)
    # t2 = Segment(m1, p1)
    # segments = [t1, t2]

    # # intersections = SweepLine(segments).intersection_points
    # # print(len(intersections))
    # # draw_lines(segments, intersections)

    # A = Vector(0, 0)
    # B = Vector(1, -1)
    # C = Vector(2, 0)
    # D = Vector(1, 1)

    # s1 = Segment(A, B)
    # s2 = Segment(B, C)
    # s3 = Segment(C, D)
    # s4 = Segment(D, A)
    # s5 = Segment(A, C)
    # s6 = Segment(B, D)
    # s7 = Segment(A, C)

    # segments = [s1, s2, s3, s4, s5, s6, Segment(
    #     Vector(-1, -2), Vector(3, 2)), Segment(Vector(0.5, 0), Vector(0.5, 2)), Segment(Vector(1.5, -2), Vector(1.5, 2)), s7]
    # A = Vector(0, 1)
    # B = Vector(1, 0)
    # C = Vector(2, 0)
    # D = Vector(3, 0)
    # E = Vector(4, 0)
    # F = Vector(5, 0)
    # s1 = Segment(A, B)
    # s2 = Segment(B, C)
    # s3 = Segment(C, D)
    # s4 = Segment(A, F)
    # segments = [s1, s2, s3, Segment(
    #     Vector(-1, 2), Vector(3, 2)), Segment(Vector(-1, 2.5), Vector(3, 2.5)), Segment(Vector(2, 2), Vector(3, 0)), Segment(Vector(-1, 0), Vector(4, 10/3))]
    # segments = [s1, s2, s3, s4]
    # # draw_lines(segments, [])
    # # sweep = SweepLine(segments)
    # # print(len(sweep.intersection_points))
    # # for point in sweep.intersection_points:
    # #     print(point)
    # # for segment in sweep.new_segments:
    # #     print(segment.min_point, segment.max_point)
    # # draw_lines(sweep.new_segments, sweep.intersection_points)
    # draw_lines(segments, [])
    # dcel = DCEL(segments)
    # print(len(dcel.faces))
