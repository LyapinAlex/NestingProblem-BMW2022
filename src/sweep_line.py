import heapq as hq
import numpy as np
import matplotlib.pyplot as plt
from class_vector import Vector, _NDIGITS
from memory_structure.class_AVL_KV import AVL_KV, Node_KV

class Segment:
    def __init__(self, p1: Vector, p2: Vector):
        if p1 < p2:
            self.begin = p1
            self.end = p2
        else:
            self.begin = p2
            self.end = p1

    def __str__(self):  # print
        return '[{}, {}]'.format(self.begin, self.end)

    def get_X(self, y):
        """По координате отрезка Y возвращает координату отрезка X,\\
            если в отрезке нет точки с координатой Y, то None"""
        if self.begin.y <= y and y <= self.end.y:
            if self.begin.y == self.end.y:
                return self.end.x  # хз что лучше возвращать в таком случае
            x0 = self.begin.x
            y0 = self.begin.y
            x1 = self.end.x
            y1 = self.end.y
            return round(((x1 - x0) / (y1 - y0)) * (y - y0) + x0, _NDIGITS)
        return None

# ----------------------------  Logical operations   ----------------------------
# лексикографический порядок (для работы headq)

    def __eq__(self, other):  # ==
        return (self.begin == other.begin) and (self.end == other.end)

    def __lt__(self, other):  # <
        return (self.begin < other.begin) or ((self.begin == other.begin) and
                                              (self.end < other.end))

    def __le__(self, other):  # <=
        return self < other or self == other

# ---------------------------  Geometric operations   ---------------------------

    def intersection_with_segments(self, other):
        """Возвращает координату пересечения пары отрезков, но\\
            если отрезки параллельны или хотя бы одна из возможных пар из их концов совпадает возвращает None"""
        a = self.end - self.begin
        b = other.begin - other.end
        c = other.begin - self.begin
        if a.psevdo_prod(b):
            l1 = c.psevdo_prod(b) / a.psevdo_prod(b)
            l2 = a.psevdo_prod(c) / a.psevdo_prod(b)
            if (0 <= l1) and (l1 <= 1) and (0 <= l2) and (l2 <= 1):
                if (0 == l1 and
                    (0 == l2 or l2 == 1)) or (1 == l1 and
                                              (0 == l2 or l2 == 1)):
                    return None
                else:
                    # inter = (self.begin + a * l1).round()
                    # if inter.x != self.get_X(inter.y) or inter.x != other.get_X(inter.y):
                    #     print("inter:", inter, "\nsegment1", self, "\nsegment2", other)
                    #     print(self.get_X(inter.y), other.get_X(inter.y))
                    return (self.begin + a * l1).round()
        return None


class Node_sweep_line(Node_KV):

    def __init__(self, key: Vector, value: Segment):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

    def __str__(self):  # print
        return 'K: {}, V:{}'.format(self.key, self.value)

    def __eq__(self, other): # ==
        return (self.key - other.key) <= 2*10**(3-_NDIGITS)

    def __lt__(self, other):  # <
        return self.key < other.key and not (self==other)

    def __gt__(self, other):  # >
        return self.key > other.key and not (self==other)

    def __le__(self, other):  # <=
        return self == other or self < other

    def __ge__(self, other):  # >=
        return self == other or self > other


class AVL_sweep_line(AVL_KV):

    def __init__(self):
        self.root = None
        self.y_scan_line = None

    def create_node(self, key, value):
        return Node_sweep_line(key, value)

    def swap_nodesKV(self, node1, node2):
        key = node1.key
        node1.key = node2.key
        node2.key = key
        value = node1.value
        node1.value = node2.value
        node2.value = value
        
    # ------------------------ n*log(n) ------------------------

    def recalculate_key_node(self, node: Node_sweep_line):
        new_key = node.value.get_X(self.y_scan_line)
        if new_key is None:
            raise Exception(
                "Ошибка: отсканированная линия ещё сканируется (в status)",
                node.value.begin, node.value.end)
        node.key = new_key
        
    def node_delete(self, node, excluded_node):
        if node is None:
            return node
        self.recalculate_key_node(node)
        if excluded_node < node:
            node.left = self.node_delete(node.left, excluded_node)
        elif excluded_node > node:
            node.right = self.node_delete(node.right, excluded_node)
        else:
            is_values_equal = False
            is_value_None = excluded_node.value is None
            if not is_value_None:
                is_values_equal = (node.value == excluded_node.value)
                node.left = self.node_delete(node.left, excluded_node)
                node.right = self.node_delete(node.right, excluded_node)

            if is_value_None or is_values_equal:
                if (node.left is None) and (node.right is None):
                    node = None
                else:
                    if self._balance(node) > 0:
                        rgt = self.max_key_node(node.left)
                        node.key = rgt.key
                        node.value = rgt.value
                        node.left = self.node_delete(node.left, rgt)
                    else:
                        rgt = self.min_key_node(node.right)
                        node.key = rgt.key
                        node.value = rgt.value
                        node.right = self.node_delete(node.right, rgt)

        if node is None:
            return node
        self._correction_height(node)
        return self.balancing_node(node)

    def node_insert(self, node, implemented_node):
        if node is None:
            return implemented_node
        self.recalculate_key_node(node)
        if implemented_node <= node:
            node.left = self.node_insert(node.left, implemented_node)
        elif implemented_node > node:
            node.right = self.node_insert(node.right, implemented_node)
        self._correction_height(node)
        return self.balancing_node(node)

    def node_find(self, node, searchable_node):
        if node is None:
            return
        self.recalculate_key_node(node)
        if node < searchable_node:
            return self.node_find(node.right, searchable_node)
        elif node > searchable_node:
            return self.node_find(node.left, searchable_node)
        else:
            is_values_equal = False
            is_value_None = searchable_node.value is None
            if not is_value_None:
                is_values_equal = (node.value == searchable_node.value)
            if is_value_None or is_values_equal:
                return node
            else:
                ans1 = self.node_find(node.left, searchable_node)
                if ans1 is None:
                    ans1 = self.node_find(node.right, searchable_node)
                return ans1

    def _find_last_turnsLR(self, node, searchable_node):
        turnsLR = [None, None]
        if node is None:
            return turnsLR
        self.recalculate_key_node(node)
        if node < searchable_node:
            turnsLR = self._find_last_turnsLR(node.right, searchable_node)
            if turnsLR[1] is None:
                turnsLR[1] = node
        elif node > searchable_node:
            turnsLR = self._find_last_turnsLR(node.left, searchable_node)
            if turnsLR[0] is None:
                turnsLR[0] = node
        if searchable_node.value is None:
            return turnsLR
        else:
            if node.value == searchable_node.value:
                return turnsLR
            else:
                if self.node_find(node.right, searchable_node) is None:
                    turnsLR = self._find_last_turnsLR(node.left, searchable_node)
                    if turnsLR[0] is None:
                        turnsLR[0] = node
                else:
                    turnsLR = self._find_last_turnsLR(node.right, searchable_node)
                    if turnsLR[1] is None:
                        turnsLR[1] = node
                return turnsLR

    # ------------------------ n**2 ------------------------

    def recalculate_key_without_changing_order(self, y):
        return self.node_recalculate_key_without_changing_order(self.root, y)

    def node_recalculate_key_without_changing_order(self,
                                                    node: Node_sweep_line, y):
        if node is None:
            return
        if node.value.get_X(y) is None:
            raise Exception(
                "Ошибка: отсканированная линия ещё сканируется (в status)",
                node.value.begin, node.value.end)
        node.key = node.value.get_X(y)
        self.node_recalculate_key_without_changing_order(node.left, y)
        self.node_recalculate_key_without_changing_order(node.right, y)


def _Error3(status: AVL_sweep_line, q):
    print(q[1],":", "segment:", q[2].begin, q[2].end)
    if q[1]==3:
        print("  :", "segment:", q[3].begin, q[3].end,'\n')
    print("координата скана:", q[0].y)
    status.inorder_print()
    raise Exception("Ошибка в поиске "+str(q[0].x))


def sweep_line(array_segments: list[Segment]):
    """не пересекаются в одной точке больше двух отрезков\\
        нет идентичных отрезков"""
    unprocessed_events = []
    intersection_points_with_dublicate = []

    def append_point(q_y, segment1: Segment, segment2: Segment):
        """Добавляю событие пересечения отрезков в unprocessed_events, если они пересекаются"""
        point = segment1.intersection_with_segments(segment2)
        if not (point is None):
            if q_y<point.y:
                hq.heappush(unprocessed_events, (point, 3, segment1, segment2))
                hq.heappush(intersection_points_with_dublicate, (point, segment1, segment2))
        return

    def is_dublicate_point(q1, q2):
        equal_segments = (q1[1]==q2[1] and q1[2]==q2[2]) or (q1[1]==q2[2] and q1[2]==q2[1])
        return equal_segments and (q1[0]==q2[0])

    def is_dublicate_event(q1, q2):
        if (q1[1]==3) and (q2[1]==3):
            equal_segments = (q1[2]==q2[2] and q1[3]==q2[3]) or (q1[2]==q2[3] and q1[3]==q2[2])
        else:
            equal_segments = q1[2] == q2[2]
        return (q1[0]==q2[0]) and (q1[1]==q2[1]) and equal_segments

    for segment in array_segments:
        hq.heappush(unprocessed_events, (segment.begin, 1, segment))
        hq.heappush(unprocessed_events, (segment.end, 2, segment))
    status = AVL_sweep_line()
    while unprocessed_events:
        q = hq.heappop(unprocessed_events)
        # удаление повторов событий
        if unprocessed_events:
            while is_dublicate_event(q, unprocessed_events[0]):
                q = hq.heappop(unprocessed_events)
                if not unprocessed_events:
                    break
        
        # пересчиать status.y_scan_line
        status.y_scan_line = q[0].y
        # status.recalculate_key_without_changing_order(q[0].y)
        ### status.inorder_print()
        if q[1] == 1:
            # добавить отрезок в status
            status.insert(q[0].x, q[2])
            # проверить его на пересечения с соседями (х2)
            neighbors = status.get_nearests(q[0].x, q[2])
            ### print("neighbors:", neighbors[0], neighbors[1])
            if not (neighbors[0] is None):
                append_point(q[0].y, q[2], neighbors[0].value)
            if not (neighbors[1] is None):
                append_point(q[0].y, q[2], neighbors[1].value)

        elif q[1] == 2:
            # проверить на пересечение новообразовавшихся соседей (х1)
            neighbors = status.get_nearests(q[0].x, q[2])
            if not ((neighbors[0] is None) or (neighbors[1] is None)):
                append_point(q[0].y, neighbors[0].value, neighbors[1].value)
            # удалить отрезок из status
            ### print(q[0].x, q[2])
            status.delete(q[0].x, q[2])

        elif q[1] == 3:  #(point, 3, segment1, segment2)
            # проверить на пересечение новообразовавшихся соседей (х2)
            node1 = status.find(q[0].x, q[2])
            neighbors1 = status.get_nearests(q[0].x, q[2])
            node2 = status.find(q[0].x, q[3])
            neighbors2 = status.get_nearests(q[0].x, q[3])
            if (node1 is None) or (node2 is None):
                _Error3(status, q)
            ### print("neighbors:", node1, node2)
            ### print("neighbors:", neighbors1[0], neighbors1[1], neighbors2[0], neighbors2[1])
            if not (neighbors1[0] is None):
                if (neighbors1[0].value != node2.value):
                    append_point(q[0].y, neighbors1[0].value, node2.value)
                else:
                    if not (neighbors1[1] is None):
                        append_point(q[0].y, neighbors1[1].value, node2.value)

            if not (neighbors2[0] is None):
                if (neighbors2[0].value != node1.value):
                    append_point(q[0].y, neighbors2[0].value, node1.value)
                else:
                    if not (neighbors2[1] is None):
                        append_point(q[0].y, neighbors2[1].value, node1.value)
            # поменять местами пересекающиеся отрезки
            status.swap_nodesKV(node1, node2)
    # удаление дубликатов точек пересечения
    intersection_points = []
    while intersection_points_with_dublicate:
        q = hq.heappop(intersection_points_with_dublicate)
        intersection_points.append(q)
        # print(intersection_points)
        if intersection_points_with_dublicate:
            while is_dublicate_point(q, intersection_points_with_dublicate[0]):
                q = hq.heappop(intersection_points_with_dublicate)
                if not intersection_points_with_dublicate:
                    break
    return intersection_points


def draw_lines(array_segments: list[Segment], intersection_points: list):
    fig, ax = plt.subplots()
    if intersection_points:
        x_values = []
        y_values = []
        for point in intersection_points:
            # print(point[1], point[2])
            x_values.append(point[0].x)
            y_values.append(point[0].y)
        ax.scatter(x_values, y_values, c = 'red', marker = 'o')
    for segment in array_segments:
        p1 = segment.begin
        p2 = segment.end
        x_values = [p1.x, p2.x]
        y_values = [p1.y, p2.y]
        plt.plot(x_values, y_values, 'b.', linestyle="--")
    plt.show()
    return 


def rundom_segments(num_segments = 10) -> list[Segment]:
    random_float_array = np.random.uniform(0, 100, size=(num_segments * 4))
    array_segments = []
    for i in range(num_segments):
        p1 = Vector(random_float_array[4*i], random_float_array[4*i+1]).round()
        p2 = Vector(random_float_array[4*i+2], random_float_array[4*i+3]).round()
        array_segments.append(Segment(p1, p2))
    return array_segments


def main():
    array_segments = rundom_segments(100)
    # draw_lines(array_segments, [])
    intersection_points = sweep_line(array_segments)
    print(len(intersection_points))
    draw_lines(array_segments, intersection_points)

    return


if __name__ == '__main__':
    for _ in range(1):
        main()


    # a0 = Vector(0, 0)
    # b0 = Vector(1, 0)
    # c0 = Vector(2, 0)
    # a1 = Vector(0, 1)
    # b1 = Vector(1, 1)
    # c1 = Vector(2, 1)
    # s1 = Segment(a0, c1)
    # s2 = Segment(b0, b1)
    # s3 = Segment(c0, a1)
    # draw_lines([s1, s2, s3], [])
    # intersection_points = sweep_line([s1, s2, s3])
    # print(len(intersection_points))
    # draw_lines([s1, s2, s3], intersection_points)


    # from math import sqrt
    # a = Vector(sqrt(2), 0.156)
    # b = Vector(1, 0)
    # s1 = Segment(a, b)
    # print(s1.get_X(0.1155))

