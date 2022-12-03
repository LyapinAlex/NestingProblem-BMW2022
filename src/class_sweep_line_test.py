
import copy
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
        return self.key != other.key and ((self.key.y < other.key.y) or ((self.key.y == other.key.y) and self.key.x > other.key.x))

    def __gt__(self, other):
        return self.key != other.key and other.__lt__(self)


# НЕ УЧТЕНО ДОБАВЛЕНИЕ НАЛАГАЮЩИХСЯ СЕГМЕНТОВ НАЧИНАЮЩИХСЯ ИЛИ КОНЧАЮЩИХСЯ В ОДНОЙ ТОЧКЕ
class EventQueue(AvlTree):
    def __init__(self, status: 'Status'):
        super().__init__()

    def insert_events_by_segment(self, segment: Segment):
        found_start_event: Event = self.find(segment.max_point)
        found_end_event: Event = self.find(segment.min_point)

        if (not found_start_event):
            event = None
            if (segment.min_point.y == segment.max_point.y):  # horizontal
                event = Event(segment.min_point)
            else:
                event = Event(segment.max_point)
            event.value.upper_segments.add(segment)
            self.insert(event)

        else:
            if (segment.min_point.y == segment.max_point.y):  # horizontal
                found_start_event.value.lower_segments.add(segment)
            else:
                found_start_event.value.upper_segments.add(segment)
        if (not found_end_event):
            event = None
            if (segment.min_point.y == segment.max_point.y):  # horizontal
                event = Event(segment.max_point)
            else:
                event = Event(segment.min_point)
            event.value.lower_segments.add(segment)
            self.insert(event)
        else:
            if (segment.min_point.y == segment.max_point.y):  # horizontal
                found_end_event.value.upper_segments.add(segment)
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
            found_event.value.inner_segments.add(segment1)
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

        if (self.key.min_point.y == self.key.max_point.y):
            return False
        if (other.key.min_point.y == other.key.max_point.y):
            return True

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
        self.event_qeue = EventQueue(self.status)
        self.new_segments = []
        self.object_handler = None

        for segment in segments:
            self.event_qeue.insert_events_by_segment(segment)
        while (self.event_qeue.root):
            event: Event = self.event_qeue.max_key_node(self.event_qeue.root)
            self.status.event_point = event.key
            key = copy.copy(event.key)  # TODO: костыль
            self.handle_event(event)
            self.event_qeue.delete(key)

    def handle_event(self, event: Event):

        # В начале считаем, что sweep_line как бы не пересекает, а проходит выше
        self.status.is_sweep_line_above_event_point = True

        self.handle_overlap_case(event)

        # Определяем эту функцию в нужном объекте и по сути обобщение готово
        self.object_handler.handle(event, self.status, self.event_qeue)

        if not (len(event.value.upper_segments) +
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
            current_max_point = collinear_segments[0].max_point

            if (current_min_point.y == current_max_point.y):  # Horizontal case
                if (current_max_point.x < prev_max_point.x):
                    self.event_qeue.delete(current_max_point)
                    return
                else:
                    event = self.event_qeue.find(current_max_point)
                    # TODO: еще надо a,b менять
                    self.status.find(
                        collinear_segments[1]).key.max_point = current_max_point
                    for elem in event.value.lower_segments:
                        if elem == collinear_segments[0]:
                            elem.min_point = current_min_point
                            break
                    self.event_qeue.delete(prev_max_point)
                    return
            else:  # Not horizontal case
                if (current_min_point > prev_min_point):
                    self.event_qeue.delete(current_min_point)
                else:
                    event = self.event_queue.find(current_min_point)
                    self.status.find(
                        collinear_segments[1]).key.min_point = current_min_point
                    for elem in event.value.lower_segments:
                        if elem == collinear_segments[0]:
                            elem.max_point = prev_max_point
                            break
                    self.event_queue.delete(prev_min_point)
                    return

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
        if (intersection is None and (intersection.y < event.key.y or intersection.y == event.key.y and intersection.x > event.key.x)):
            self.event_queue.insert_event_by_intersection(
                intersection, first_segment, second_segment)
