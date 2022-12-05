from copy import deepcopy
import copy
from matplotlib import pyplot as plt

import numpy as np
from class_Dcel_sweep_line import Event, EventQueue, Status, StatusNode, StatusValue, SweepLine
from class_direction import Direction, psevdoProd
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
        if (value in None):
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


class DcelStatusNode(StatusNode):
    def __init__(self, key, value=None):
        if (value is None):
            value = DcelStatusValue()
        super().__init__(key, value)
        self.init_half_edges(key)

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

    def __call__(self, current_event: DcelEvent, event_qeue, status: DcelStatus) -> None:

        # Один из сегментов проходит через другой, лежит на нем и т.д. . Это не обязательно пересечение, к примеру [0,1],[1,2] не пройдут это условие

        # Каждый Event обходится ровно один раз, тем самым мы можем спокойно инициализировать Vertex
        vertex: Vertex = self.create_new_vertex(current_event, status)

        if (len(current_event.value.inner_segments) > 1):
            self.split_half_edges(vertex, current_event, status)

    def create_new_vertex(self, event, status):
        vertex = Vertex(event.key)
        event.value.vertex = vertex

        # Добавляем в Vertex half_edges в котором они начинаются
        rightmost_status = None
        for segment in event.value.inner_segments:
            found_status = status.find(segment)
            if (rightmost_status is None or rightmost_status < found_status):
                rightmost_status = found_status

        for segment in event.value.lower_segments:
            found_status = status.find(segment)

            if (rightmost_status is None or rightmost_status < found_status):
                rightmost_status = found_status

            if (vertex.key == found_status.value.half_edge.origin):
                self.dcel.half_edges.append(found_status.value.half_edge)
                vertex.add_half_edge(self.dcel.half_edges[-1])
                self.dcel.half_edges.append(found_status.twin_half_edge)
                other_vertex = self.dcel.vertices.find(
                    found_status.value.half_edge.end)
                other_vertex.add_half_edge(self.dcel.half_edges[-1])
            else:
                self.dcel.half_edges.append(found_status.value.twin_half_edge)
                vertex.add_half_edge(self.dcel.half_edges[-1])
                self.dcel.half_edges.append(found_status.value.half_edge)
                other_vertex = self.dcel.vertices.find(
                    found_status.value.half_edge.origin)
                other_vertex.add_half_edge(self.dcel.half_edges[-1])

        right_neighbour = None
        if (rightmost_status):
            right_neighbour, _ = status.get_nearests(rightmost_status.key)

        if (right_neighbour is not None):
            # TODO: Я пока не понимаю какой из HalfEdges сюда вставлять
            vertex.value.right_half_edge = None

        self.dcel.vertices.insert(vertex)
        return vertex

    def split_half_edges(self, vertex: 'Vertex', event, status):

        for segment in event.value.inner_segments:
            found_status = status.find(segment)
            # Не уверен, что нужно копировать, но на всякий случай
            prev_end = copy.copy(found_status.value.half_edge.end)

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

    def handle_upper(self):
        pass

    def handle_inner(self):
        pass

    def handle_lower(self):
        pass


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
        for i in range(len(self.value.half_edges_by_ccw_angle)):
            if (self.value.half_edges_by_ccw_angle[i].direction > half_edge.direction):
                self.value.half_edges_by_ccw_angle.insert(i, half_edge)
                return
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


class Verticies(AvlTree):
    def __init__(self):
        super().__init__()

    def create_node(self, key):
        node = Vertex(key)
        return node

# class Vertex:  # OK
#     def __init__(self, point: Vector):
#         self.point = point
#         self.half_edges_by_ccw_angle: list[HalfEdge] = []
#         self.right_half_edge: HalfEdge = None

#     def add_half_edge(self, half_edge):
#         for i in range(len(self.half_edges_by_ccw_angle)):
#             if (self.half_edges_by_ccw_angle[i].direction > half_edge.direction):
#                 self.half_edges_by_ccw_angle.insert(i, half_edge)
#                 return
#         self.half_edges_by_ccw_angle.append(half_edge)


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
        self.is_visited = False

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

        twin_half_edge.origin = edge.max_point
        twin_half_edge.end = edge.min_point

        half_edge.direction = Direction(edge.min_point-edge.max_point)
        twin_half_edge.direction = Direction(edge.max_point-edge.min_point)

        return half_edge, twin_half_edge


class Face:  # OK
    def __init__(self, half_edge=None):
        self.boundary_half_edge: HalfEdge = half_edge
        self.holes_half_edges: list[HalfEdge] = []
        self.label = None


class DCEL:
    def __init__(self, edges: list[tuple[Vector, Vector]] = []) -> None:
        self.unbounded_face: Face = None
        self.faces: list[Face] = []
        self.vertices: Verticies = Verticies()
        self.half_edges: list[HalfEdge] = []
        self.build_dcel(edges)

    def build_dcel(self, edges):
        # Начальная инициализация
        status = DcelStatus()
        event_qeue = EventQueue()
        handler = BuildHandler(self)
        sweep_line = SweepLine(edges, status, event_qeue, handler)

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

    @staticmethod
    def subdivision(d1: 'DCEL', d2: 'DCEL') -> 'DCEL':  # NOT OK
        subdiv = DCEL()
        subdiv.half_edges = deepcopy(d1.half_edges+d2.half_edges)
        subdiv.vertices = deepcopy(d1.vertices | d2.vertices)

        def handle_event(event, event_type):
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
        plt.plot(x_values, y_values, 'b.', linestyle="--")
    if (current_segments):
        for segment in current_segments:
            p1 = segment.min_point
            p2 = segment.max_point
            x_values = [p1.x, p2.x]
            y_values = [p1.y, p2.y]
            plt.plot(x_values, y_values, 'r.', linestyle="--")
    if (left_neighbour):
        p1 = left_neighbour.min_point
        p2 = left_neighbour.max_point
        x_values = [p1.x, p2.x]
        y_values = [p1.y, p2.y]
        plt.plot(x_values, y_values, 'g.', linestyle="--")
    if (right_neighbour):
        p1 = right_neighbour.min_point
        p2 = right_neighbour.max_point
        x_values = [p1.x, p2.x]
        y_values = [p1.y, p2.y]
        plt.plot(x_values, y_values, 'g.', linestyle="--")
    plt.show()
    return


def main():
    array_segments = rundom_segments(10)
    dcel = DCEL(array_segments)
    print(len(dcel.half_edges))
    draw_lines(array_segments, [])
    # sweep_line = SweepLine(array_segments, Status(), EventQueue())
    # sweep_line.event_queue.inorder_print()
    # print(len(sweep_line.intersection_points))
    # draw_lines(array_segments, sweep_line.intersection_points)


if __name__ == '__main__':
    main()
#     segments1 = [[Vector(0, 0), Vector(1, 0)], [Vector(1, 0), Vector(1, 1)], [
#         Vector(1, 1), Vector(0, 1)], [Vector(0, 1), Vector(0, 0)]]
#     segments2 = [[Vector(0.5, 0), Vector(1.5, 0)], [Vector(1.5, 0), Vector(1.5, 1)], [
#         Vector(1.5, 1), Vector(0.5, 1)], [Vector(0.5, 1), Vector(1.5, 0)]]
#     dcel1 = DCEL()
#     dcel2 = DCEL()

#     for seg in segments1:
#         dcel1.add_edge(seg)
#     for seg in segments2:
#         dcel2.add_edge(seg)
#     dcel2.init_faces()
#     dcel1.init_faces()
#     #log_and = DCEL.logical_and(dcel1, dcel2)
#     # log_and.draw()
#     log_or = DCEL.logical_or(dcel1, dcel2)
#    # log_or.draw()
#     log_min = DCEL.logical_minus(dcel1, dcel2)
#     # log_min.draw()
#     print()
