
import copy
from class_segment import Segment
from class_vector import Vector
from memory_structure.class_AVL_tree import Node
from memory_structure.class_AVL_tree import AvlTree

_NDIGITS = 6


class Event(Node):
    def __init__(self, point):
        super().__init__(point)
        self.upper_segments = set()
        self.inner_segments = set()
        self.lower_segments = set()

    def swap(self: 'Event', other: 'Event'):
        key = self.key
        inner_segments = self.inner_segments
        upper_segments = self.upper_segments
        lower_segments = self.lower_segments

        self.key = other.key

        self.lower_segments = other.lower_segments
        self.inner_segments = other.inner_segments
        self.upper_segments = other.upper_segments

        other.key = key
        other.inner_segments = inner_segments
        other.lower_segments = lower_segments
        other.upper_segments = upper_segments


class EventQueue(AvlTree):
    def __init__(self, status: 'Status'):
        super().__init__()

    def insert_events_by_segment(self, segment: Segment):
        found_start_event: Event = self.find(segment.max_point)
        found_end_event: Event = self.find(segment.min_point)

        if (not found_start_event):
            event = Event(segment.max_point)
            event.upper_segments.add(segment)
            self.insert(event)

        else:
            found_start_event.upper_segments.add(segment)
        if (not found_end_event):
            event = Event(segment.min_point)
            event.lower_segments.add(segment)
            self.insert(event)
        else:
            found_end_event.lower_segments.add(segment)

    def insert_event_by_intersection(self, point, segment1, segment2):
        found_event: Event = self.find(point)
        if (not found_event):
            event = Event(point)
            event.inner_segments.add(segment1)
            event.inner_segments.add(segment2)
            self.insert(event)
        else:
            found_event.inner_segments.add(segment1)
            found_event.inner_segments.add(segment2)


class StatusNode(Node):
    def __init__(self, key):
        super().__init__(key)
        self.status: Status = None

    def __lt__(self: 'StatusNode', other: 'StatusNode'):  # <
        dist1 = self.key.compare_with_point(self.status.event_point)
        dist2 = other.key.compare_with_point(other.status.event_point)

        if (self.key.max_point.y == self.status.event_point.y and other.key.max_point.y == self.status.event_point.y or dist1 == 0 and dist2 == 0):
            return self.key.max_point < other.key.max_point
        elif (self.key.max_point.y == self.status.event_point.y):
            return True if dist2 == 1 else False
        elif (other.key.max_point.y == self.status.event_point.y):
            return True if dist1 == -1 else False
        return True if dist2 == 1 else False

    def __gt__(self, other):  # >
        return other < self and self.key.max_point != other.key.max_point and self.key.min_point != other.key.min_point


class Status(AvlTree):
    def __init__(self):
        super().__init__()
        self.event_queue = None
        self.event_point: Vector = None

    def create_node(self, key):
        node = StatusNode(key)
        node.status = self
        return node


class SweepLine:
    def __init__(self, segments: list[Segment]) -> None:
        self.intersection_points = []
        self.status = Status()
        self.event_queue = EventQueue(self.status)
        self.i = 0
        for segment in segments:
            self.event_queue.insert_events_by_segment(segment)
        while (self.event_queue.root):
            event: Event = self.event_queue.max_key_node(self.event_queue.root)
            copy_event = copy.copy(event)  # костыль
            self.status.event_point = event.key
            self.event_queue.delete(event.key)
            self.handle_event(copy_event)

    def handle_event(self, event: Event):
        upper_segments = event.upper_segments
        lower_segments = event.lower_segments
        inner_segments = event.inner_segments
        if (len(upper_segments)+len(lower_segments)+len(inner_segments) > 1):
            self.intersection_points.append(event.key)

        for segment in lower_segments:  # Удаляем лишние сегменты
            self.status.delete(segment)

        inner_segments = sorted(list(inner_segments),
                                key=lambda segment: segment.max_point.x)

        # Удаление и вставка O(k*log(k)), так что так же эффективно
        reversed_inner_segments = list(reversed(inner_segments))

        # Свапаем сегменты проходящие через точку
        for i in range(len(inner_segments)//2):
            self.status.swap(self.status.find(
                inner_segments[i]), self.status.find(reversed_inner_segments[i]))

        for segment in upper_segments:  # Вставляем upper segments
            status = StatusNode(segment)
            status.status = self.status
            self.status.insert(status)

        if (len(upper_segments)+len(inner_segments) == 0):
            right_neighbour, left_neighbour = self.status.get_nearests(  # Исправить
                Segment(event.key.x, event.key.y+1000, self.i))
            self.i += 1
            if (left_neighbour != None and right_neighbour != None):
                intersection = Segment.intersection(
                    left_neighbour.key, right_neighbour.key)
                if (intersection and intersection.y < event.key.y):
                    self.event_queue.insert_event_by_intersection(
                        event, left_neighbour.key, right_neighbour.key)
        else:
            rightmost = None
            leftmost = None

            upper_segments = sorted(
                list(upper_segments), key=lambda segment: segment.min_point.x)  # Снова k*log(k) со swap'ом было бы тоже самое
            rightmost = upper_segments[-1] if len(
                upper_segments) != 0 else None
            leftmost = upper_segments[0] if len(upper_segments) != 0 else None

            if (not rightmost or len(inner_segments) != 0 and upper_segments[-1].min_point.x > inner_segments[-1].min_point.x):
                rightmost = inner_segments[-1]

            if (not leftmost or len(inner_segments) and upper_segments[0].min_point.x < inner_segments[0].min_point.x):
                leftmost = inner_segments[-1]

            if (leftmost):
                _, left_neighbour = self.status.get_nearests(leftmost)
                if (left_neighbour):
                    left_neighbour = left_neighbour.key
                    intersection = Segment.intersection(
                        left_neighbour, leftmost)
                    if (intersection and intersection.y < event.key.y):
                        self.event_queue.insert_event_by_intersection(
                            intersection, leftmost, left_neighbour)

            if (rightmost):
                right_neighbour, _ = self.status.get_nearests(rightmost)
                if (right_neighbour):
                    right_neighbour = right_neighbour.key
                    intersection = Segment.intersection(
                        right_neighbour, rightmost)
                    if (intersection and intersection.y < event.key.y):
                        self.event_queue.insert_event_by_intersection(
                            intersection, rightmost, right_neighbour)


def draw_lines(array_segments: list[Segment], intersection_points: list):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    if intersection_points:
        x_values = []
        y_values = []
        for point in intersection_points:
            x_values.append(point[0].x)
            y_values.append(point[0].y)
        ax.scatter(x_values, y_values, c='red', marker='o')
    for segment in array_segments:
        p1 = segment.min_point
        p2 = segment.max_point
        x_values = [p1.x, p2.x]
        y_values = [p1.y, p2.y]
        plt.plot(x_values, y_values, 'b.', linestyle="--")
    plt.show()
    return


def rundom_segments(num_segments=10) -> list[Segment]:
    import numpy as np
    random_float_array = np.random.uniform(0, 100, size=(num_segments * 4))
    array_segments = []
    for i in range(num_segments):
        p1 = Vector(random_float_array[4*i], random_float_array[4*i+1]).round()
        p2 = Vector(random_float_array[4*i+2],
                    random_float_array[4*i+3]).round()
        array_segments.append(Segment(p1, p2, i))
    return array_segments


def main():
    array_segments = rundom_segments(100)
    draw_lines(array_segments, [])
    sweep_line = SweepLine(array_segments)
    print(len(sweep_line.intersection_points))
    draw_lines(array_segments, sweep_line.intersection_points)


if __name__ == '__main__':
    # main()
    # ТЕСТЫ
    a0 = Vector(0, 0)
    b0 = Vector(1, 0)
    c0 = Vector(2, 0)
    a1 = Vector(0, 1)
    b1 = Vector(1, 1)
    c1 = Vector(2, 1)
    s1 = Segment(a0, c1, 1)
    s2 = Segment(b0, b1, 2)
    s3 = Segment(c0, a1, 3)
    segments = [s1, s2, s3]

    # v1 = Vector(1, 1)
    # v0 = 0*v1
    # v2 = 2*v1
    # v3 = 3*v1
    # w1 = Segment(v0, v2, 4)
    # w2 = Segment(v0, b0, 5)
    # segments = [w1, w2]

    # m0 = Vector(0, 1)
    # m1 = Vector(1, 0)
    # p0 = Vector(2, 1)
    # p1 = Vector(1, 2)
    # t1 = Segment(m0, p0, 6)
    # t2 = Segment(m1, p1, 7)
    # segments = [t1, t2]

    intersections = SweepLine(segments).intersection_points
    print(len(intersections))
    draw_lines(segments, intersections)
