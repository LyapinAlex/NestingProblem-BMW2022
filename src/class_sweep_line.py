
import copy

from matplotlib import pyplot as plt
import numpy as np
from class_direction import is_collinear
from class_segment import Segment
from class_vector import Vector
from memory_structure.class_AVL_tree import Node
from memory_structure.class_AVL_tree import AvlTree


class EventValue:  # OK
    def __init__(self) -> None:
        self.upper_segments = set()
        self.inner_segments = set()
        self.lower_segments = set()


class Event(Node):  # OK
    def __init__(self, point):
        super().__init__(point, EventValue())

    # Чтобы при одинаковых y извлекалась сначала самая левая точка, а не правая
    def __lt__(self: 'Event', other: 'Event'):
        return self.key != other.key and self.key < other.key

    def __gt__(self, other):
        return self.key != other.key and other.__lt__(self)


# НЕ УЧТЕНО ДОБАВЛЕНИЕ НАЛАГАЮЩИХСЯ СЕГМЕНТОВ НАЧИНАЮЩИХСЯ ИЛИ КОНЧАЮЩИХСЯ И ОКАНСИВАЮЩИХСЯ В ОДНОЙ ТОЧКЕ
class EventQueue(AvlTree):
    def __init__(self, status: 'Status'):
        super().__init__()

    def insert_events_by_segment(self, segment: Segment):
        found_start_event: Event = self.find(segment.max_point)
        found_end_event: Event = self.find(segment.min_point)

        collinear_segment = None

        if (found_start_event):
            for seg in found_start_event.value.upper_segments:
                if is_collinear(seg.max_point - seg.min_point, segment.max_point - segment.min_point):
                    collinear_segment = seg
                    break

        if (not collinear_segment and found_end_event):
            for seg in found_end_event.value.lower_segments:
                if is_collinear(seg.max_point - seg.min_point, segment.max_point - segment.min_point):
                    collinear_segment = seg
                    break
        if (collinear_segment):
            if (collinear_segment.max_point == segment.max_point):  # Совпадают start point'ы\
                if (collinear_segment.min_point < segment.min_point):  # Забиваем на это, никакой новой информации мы не получим
                    return
                else:
                    new_segment = Segment(
                        collinear_segment.min_point, segment.min_point, 0)
                    self.insert_events_by_segment(new_segment)
                    return
            if (collinear_segment.min_point == segment.min_point):  # Совпадают end point'ы
                # Забиваю на это, никакой новой информации мы не получим
                if (collinear_segment.max_point > segment.max_point):
                    return
                else:
                    new_segment = Segment(
                        collinear_segment.max_point, segment.max_point, 0)
                    self.insert_events_by_segment(new_segment)
                    return

        if (not found_start_event):
            event = Event(segment.max_point)
            event.value.upper_segments.add(segment)
            self.insert(event)
        else:
            found_start_event.value.upper_segments.add(segment)

        if (not found_end_event):
            event = Event(segment.min_point)
            event.value.lower_segments.add(segment)
            self.insert(event)
        else:
            found_end_event.value.lower_segments.add(segment)

    def insert_event_by_intersection(self, point, segment1, segment2):
        found_event: Event = self.find(point)
        if (not found_event):
            event = Event(point)
            event.value.inner_segments.add(segment1)
            event.value.inner_segments.add(segment2)
            self.insert(event)
        else:
            if (segment1.max_point != found_event.key and segment1.min_point != found_event.key):
                found_event.value.inner_segments.add(segment1)
            if (segment2.max_point != found_event.key and segment2.min_point != found_event.key):
                found_event.value.inner_segments.add(segment2)

    def create_node(self, key):
        return Event(key)


class StatusValue:  # OK
    def __init__(self) -> None:
        self.status = None


class StatusNode(Node):  # TODO

    def __init__(self, key):
        super().__init__(key, StatusValue())

    def __lt__(self: 'StatusNode', other: 'StatusNode'):
        '''Имеем следующий инвариант dist1==0 or dist2 ==0, то есть хотя бы один сегмент при
        сравнении будет проходящим через точку (Потому что только такие мы ищем, вставляем и удаляем)'''
        dist1 = self.key.compare_with_point(self.value.status.event_point)
        dist2 = other.key.compare_with_point(self.value.status.event_point)

        if (dist1 != 0):  # self не проходит через точку, значит other проходит, и точка должна лежать справа от self
            return dist1 == -1

        if (dist2 != 0):  # other не проходит через точку, значит self проходит, и точка должна лежать слева от other
            return dist2 == 1

        # TODO: Поправить для горизонтальный сегментов

        # Случай двух горизонтальных (Только для поиска, для пересекающихся одновременно не могут быть в дереве)
        if (self.key.min_point.y == self.key.max_point.y and other.key.max_point.y == other.key.min_point.y):
            return False

        # Если self - горизонтальный, то он меньше всех
        # if (self.key.min_point.y == self.key.max_point.y):
        #     return True
        # # Если other - горизонтальный, то он меньше всех
        # if (other.key.min_point.y == other.key.max_point.y):
        #     return False

        # Если и self и other проходят через точку, то порядок определяется малым отклонением sweep_line (ненастоящим) по оси y

        if (self.value.status.is_sweep_line_above_event_point):
            # Если порядок определяется верхним отклонением
            # То максимальная точка self должна лежать слева от other

            dist = other.key.compare_with_point(self.key.max_point)
            return dist == 1
        else:
            # Если порядок определяется нижним отклонением
            # То минимальная точка self должна лежать слева от other

            dist = other.key.compare_with_point(self.key.min_point)
            return dist == 1

    def __gt__(self, other):  # >
        return self.key != other.key and other.__lt__(self)


class Status(AvlTree):
    def __init__(self):
        super().__init__()
        self.event_queue = None
        self.event_point: Vector = None
        self.is_sweep_line_above_event_point = True

    def create_node(self, key):
        node = StatusNode(key)
        node.value.status = self
        return node


class SweepLine:
    def __init__(self, segments: list[Segment]) -> None:
        self.intersection_points = []
        self.status = Status()
        self.event_queue = EventQueue(self.status)
        self.new_segments = []
        self.object_handler = None

        for segment in segments:
            self.event_queue.insert_events_by_segment(segment)
        while (self.event_queue.root):
            event: Event = self.event_queue.max_key_node(self.event_queue.root)
            self.status.event_point = event.key
            key = copy.copy(event.key)  # TODO: костыль
            self.handle_event(event)
            self.event_queue.delete(key)

    def handle_event(self, event: Event):

        # В начале считаем, что sweep_line как бы не пересекает, а проходит выше
        self.status.is_sweep_line_above_event_point = True

        # Фиктивный event порожденный наложением
        if (len(event.value.inner_segments) == 1 and len(event.value.lower_segments)+len(event.value.upper_segments) == 0):
            return

        # Определяем эту функцию в нужном объекте и по сути обобщение готово
        # self.object_handler.handle(event, self.status, self.event_queue)

        if (self.handle_overlap_case(event)):
            return

        # Если какой-то сегмент проходит через upper_segments (Только один, то есть еще пересечение не было найдено, а оно есть)
        if (len(event.value.inner_segments) == 0 and len(event.value.lower_segments) == 0):
            self.check_on_new_inner_segments(event)

        if (len(event.value.upper_segments) +
                len(event.value.lower_segments) +
                len(event.value.inner_segments) > 1):
            self.handle_intersection_case(event)

        self.remove_lower_segments(event)

        self.reverse_inner_segments(event)

        self.insert_upper_segments(event)

        if (len(event.value.upper_segments)+len(event.value.inner_segments) == 0):
            self.handle_only_lower_segments_case(event)
        else:
            self.handle_upper_inner_segments_case(event)

    def check_on_new_inner_segments(self, event):
        fictive_segment = Segment(
            event.key+Vector(0, -1000), event.key+Vector(0, 1000), 0)  # Можно ли убрать id ?
        fictive_status = StatusNode(fictive_segment)
        fictive_status.value.status = self.status
        right_neighbour, left_neighbour = self.status.get_nearests(
            fictive_segment)
        if left_neighbour is not None:
            left_neighbour = left_neighbour.key
        if right_neighbour is not None:
            right_neighbour = right_neighbour.key
        self.status.delete(fictive_segment)

        if (left_neighbour is not None and left_neighbour.compare_with_point(event.key) == 0):
            event.value.inner_segments.add(left_neighbour)
            return
        if (right_neighbour is not None and right_neighbour.compare_with_point(event.key) == 0):
            event.value.inner_segments.add(right_neighbour)
            return

        if (left_neighbour is not None and right_neighbour is not None):
            self.find_new_event(event, left_neighbour, right_neighbour)

    def handle_overlap_case(self, event):
        collinear_segments = None

        for segment in event.value.upper_segments:
            collinear_segment_status = self.status.find(segment)
            if (collinear_segment_status is not None and collinear_segment_status.key != segment):
                collinear_segments = [segment, collinear_segment_status.key]
                break

        """Верхняя точка нового сегмента точно меньше старого, значит ее можно удалить,
         нижняя точка может быть ниже, а может быть выше. Надо найти большую из них, удалить ее,
          а в другой поменять сегмент на новый, кроме того надо отдельно обработать горизонтальный случай"""

        if (collinear_segments is not None):
            prev_min_point = collinear_segments[1].min_point
            current_min_point = collinear_segments[0].min_point
            prev_max_point = collinear_segments[1].max_point

            if (current_min_point > prev_min_point):
                event = self.event_queue.find(current_min_point)
                event.value.lower_segments.remove(collinear_segments[0])
                event.value.inner_segments.add(collinear_segments[1])
                return True
            else:
                event = self.event_queue.find(current_min_point)
                prev_event = self.event_queue.find(prev_min_point)
                status = self.status.find(collinear_segments[1])
                status.key.min_point = current_min_point
                for elem in event.value.lower_segments:
                    if elem == collinear_segments[0]:
                        elem.max_point = prev_max_point
                        break
                prev_event.value.lower_segments.remove(collinear_segments[1])
                prev_event.value.inner_segments.add(status.key)
                return True
        return False

    def handle_intersection_case(self, event):
        self.intersection_points.append(event.key)

    def remove_lower_segments(self, event):
        for segment in event.value.lower_segments:
            self.new_segments.append(segment)
            self.status.delete(segment)

    def reverse_inner_segments(self, event):
        for segment in event.value.inner_segments:
            self.status.delete(segment)

        self.status.is_sweep_line_above_event_point = False

        for segment in event.value.inner_segments:
            status = StatusNode(segment)
            status.value.status = self.status
            self.status.insert(status)

    def insert_upper_segments(self, event):
        for segment in event.value.upper_segments:
            status = StatusNode(segment)
            status.value.status = self.status
            self.status.insert(status)

    def handle_only_lower_segments_case(self, event):
        fictive_segment = Segment(
            event.key+Vector(0, -1000), event.key+Vector(0, 1000), 0)  # Можно ли убрать id ?
        fictive_status = StatusNode(fictive_segment)
        fictive_status.value.status = self.status
        right_neighbour, left_neighbour = self.status.get_nearests(
            fictive_segment)

        if left_neighbour is not None:
            left_neighbour = left_neighbour.key
        if right_neighbour is not None:
            right_neighbour = right_neighbour.key
        self.status.delete(fictive_segment)

        if (left_neighbour is not None and right_neighbour is not None):
            self.find_new_event(event, left_neighbour, right_neighbour)

    def handle_upper_inner_segments_case(self, event):
        rightmost = None  # max(U(e),I(e))
        leftmost = None  # min(U(e),I(e))

        upper_segments_status = []
        inner_segments_status = []

        for segment in event.value.upper_segments:
            status = StatusNode(segment)
            status.value.status = self.status
            upper_segments_status.append(status)

        for segment in event.value.inner_segments:
            status = StatusNode(segment)
            status.value.status = self.status
            inner_segments_status.append(status)

        upper_segments_status.sort()  # Сортируем чтобы выбрать самое правое и левое
        inner_segments_status.sort()

        # Ищем самого правого и самого левого

        rightmost = upper_segments_status[-1].key if len(
            upper_segments_status) != 0 else None
        leftmost = upper_segments_status[0].key if len(
            upper_segments_status) != 0 else None

        if (rightmost is None and len(inner_segments_status) != 0 or len(inner_segments_status) != 0 and upper_segments_status[-1] > inner_segments_status[-1]):
            rightmost = inner_segments_status[-1].key

        if (leftmost is None and len(inner_segments_status) != 0 or len(inner_segments_status) and upper_segments_status[0] < inner_segments_status[0]):
            leftmost = inner_segments_status[0].key

        if (leftmost is not None):
            _, left_neighbour = self.status.get_nearests(leftmost)

            if (left_neighbour is not None):
                left_neighbour = left_neighbour.key
                self.find_new_event(event, leftmost, left_neighbour)

        if (rightmost):
            right_neighbour, _ = self.status.get_nearests(rightmost)

            if (right_neighbour):
                right_neighbour = right_neighbour.key
                self.find_new_event(event, rightmost, right_neighbour)

    def find_new_event(self, event, first_segment, second_segment):
        intersection = Segment.intersection(first_segment, second_segment)
        if (intersection is not None and (intersection.y < event.key.y or intersection.y == event.key.y and intersection.x < event.key.x)):
            self.event_queue.insert_event_by_intersection(
                intersection, first_segment, second_segment)


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


def rundom_segments(num_segments=10) -> list[Segment]:
    random_float_array = np.random.uniform(
        0, 100, size=(num_segments * 4))
    A = Vector(0, 50)
    B = Vector(20, 50)
    C = Vector(40, 50)
    D = Vector(60, 50)
    E = Vector(80, 50)
    F = Vector(100, 50)
    s1 = Segment(A, B, 0)
    s2 = Segment(B, C, 1)
    s3 = Segment(C, D, 2)
    s4 = Segment(A, F, 3)
    array_segments = [s1, s2, s3, s4]
    for i in range(num_segments):
        p1 = Vector(
            float(random_float_array[4*i]), float(random_float_array[4*i+1])).round()
        p2 = Vector(float(random_float_array[4*i+2]),
                    float(random_float_array[4*i+3])).round()
        array_segments.append(Segment(p1, p2, i))
    return array_segments


def main():
    array_segments = rundom_segments(100)
    draw_lines(array_segments, [])
    sweep_line = SweepLine(array_segments)
    sweep_line.event_queue.inorder_print()
    print(len(sweep_line.intersection_points))
    draw_lines(array_segments, sweep_line.intersection_points)


if __name__ == '__main__':
    main()
    # ТЕСТЫ
    # a0 = Vector(0, 0)
    # b0 = Vector(1, 0)
    # c0 = Vector(2, 0)
    # a1 = Vector(0, 1)
    # b1 = Vector(1, 1)
    # c1 = Vector(2, 1)
    # s1 = Segment(a0, c1, 1)
    # s2 = Segment(b0, b1, 2)
    # s3 = Segment(c0, a1, 3)
    # s1 = Segment(Vector(0, 0), Vector(1, 1), 0)
    # s2 = Segment(Vector(0, -1), Vector(1, 0), 1)
    # s3 = Segment(Vector(0.7, -2), Vector(0.3, 1), 2)
    # s4 = Segment(Vector(0, -3), Vector(1, 2.5), 2)

    # segments = [s1, s2, s3]
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

    # intersections = SweepLine(segments).intersection_points
    # print(len(intersections))
    # draw_lines(segments, intersections)

    # A = Vector(0, 0)
    # B = Vector(1, -1)
    # C = Vector(2, 0)
    # D = Vector(1, 1)

    # s1 = Segment(A, B, 0)
    # s2 = Segment(B, C, 1)
    # s3 = Segment(C, D, 2)
    # s4 = Segment(D, A, 3)
    # s5 = Segment(A, C, 4)
    # s6 = Segment(B, D, 5)
    # s7 = Segment(A, C, 12)

    # segments = [s1, s2, s3, s4, s5, s6, Segment(
    #     Vector(-1, -2), Vector(3, 2), 6), Segment(Vector(0.5, 0), Vector(0.5, 2), 7), Segment(Vector(1.5, -2), Vector(1.5, 2), 7), s7]
    # A = Vector(0, 1)
    # B = Vector(1, 0)
    # C = Vector(2, 0)
    # D = Vector(3, 0)
    # E = Vector(4, 0)
    # F = Vector(5, 0)
    # s1 = Segment(A, B, 0)
    # s2 = Segment(B, C, 1)
    # s3 = Segment(C, D, 2)
    # s4 = Segment(A, F, 3)
    # segments = [s1, s2, s3, Segment(
    #     Vector(-1, 2), Vector(3, 2), 3), Segment(Vector(-1, 2.5), Vector(3, 2.5), 3), Segment(Vector(2, 2), Vector(3, 0), 4), Segment(Vector(-1, 0), Vector(4, 10/3), 5)]
    # segments = [s1, s2, s3, s4]
    # draw_lines(segments, [])
    # sweep = SweepLine(segments)
    # print(len(sweep.intersection_points))
    # for point in sweep.intersection_points:
    #     print(point)
    # for segment in sweep.new_segments:
    #     print(segment.min_point, segment.max_point)
    # draw_lines(sweep.new_segments, sweep.intersection_points)
