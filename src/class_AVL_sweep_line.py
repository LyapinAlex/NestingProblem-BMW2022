import heapq as hq
import numpy as np
from class_vector import Vector, _NDIGITS
from memory_structure.class_AVL import AVL, Node

class Segment:
    def __init__(self, p1: Vector, p2: Vector, id):
        if p1 < p2:
            self.begin = p1
            self.end = p2
        else:
            self.begin = p2
            self.end = p1
        self.id = id

    def __str__(self):  # print
        return '[{}, {}]'.format(self.begin, self.end)

    def __repr__(self):
        return 'Segment({}, {})'.format(self.begin, self.end)
    
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

    def distance_point_from_segment(self, point: Vector):
        a = self.end - self.begin
        b = point - self.begin
        return a.psevdo_prod(b)

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
                if (0 == l1 and (0 == l2 or l2 == 1)) or (1 == l1 and (0 == l2 or l2 == 1)):
                    return None
                else:
                    # inter = (self.begin + a * l1).round()
                    # if inter.x != self.get_X(inter.y) or inter.x != other.get_X(inter.y):
                    #     print("inter:", inter, "\nsegment1", self, "\nsegment2", other)
                    #     print(self.get_X(inter.y), other.get_X(inter.y))
                    return (self.begin + a * l1).round()
        return None

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


class Node_sweep_line(Node):
    def __init__(self, key: Segment):
        self.key = key
        self.event = None
        self.left = None
        self.right = None
        self.height = 1

    # ----------------------------  Logical operations   ----------------------------
    
    def __lt__(self, other):  # <
        dist = other.key.distance_point_from_segment(self.event[0])
        return dist > 0 and (abs(dist) > 10**(2-_NDIGITS))

    def __gt__(self, other):  # >
        dist = other.key.distance_point_from_segment(self.event[0])
        return dist < 0 and (abs(dist) > 10**(2-_NDIGITS))


class AVL_sweep_line(AVL):
    def __init__(self):
        self.root = None
        self.event = [Vector(0,0)]

    def change_event(self, new_event):
        self.event[0] = new_event

    def create_node(self, key):
        a = Node_sweep_line(key)
        a.event = self.event
        return a

    def node_find(self, node, searchable_node):
        if node is None:
            return None
        if searchable_node > node: #!
            return self.node_find(node.right, searchable_node)
        elif searchable_node < node: #!
            return self.node_find(node.left, searchable_node)
        else:
            if (node == searchable_node):
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
        if searchable_node > node: #!
            turnsLR = self._find_last_turnsLR(node.right, searchable_node)
            if turnsLR[1] is None:
                turnsLR[1] = node
        elif searchable_node < node: #!
            turnsLR = self._find_last_turnsLR(node.left, searchable_node)
            if turnsLR[0] is None:
                turnsLR[0] = node
        if node == searchable_node:
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

    def node_insert(self, node, implemented_node):
        if node is None:
            return implemented_node
        elif implemented_node > node: #!
            node.right = self.node_insert(node.right, implemented_node)
        else: #!
            node.left = self.node_insert(node.left, implemented_node)
        self._correction_height(node)
        return self.balancing_node(node)

    def node_delete(self, node, excluded_node):
        if node is None:
            return node
        elif excluded_node < node: #!
            node.left = self.node_delete(node.left, excluded_node)
        elif excluded_node > node: #!
            node.right = self.node_delete(node.right, excluded_node)
        else:
            if (node == excluded_node):
                if (node.left is None) and (node.right is None):
                    node = None
                else:
                    if self._balance(node) > 0:
                        # rgt = self.max_key_node(node.left) # можно убрать "костыль 1" если удалять прямо здесь (новую аналогичную функцию создать)
                        # node.key = rgt.key
                        # current_event = self.event[0] #костыль 1
                        # self.change_event(Vector(rgt.key.get_X(self.event[0].y), self.event[0].y)) #костыль 1
                        # node.left = self.node_delete(node.left, rgt) 
                        # self.change_event(current_event) #костыль 1
                        rgt = self.max_key_node(node.left)
                        node.key = rgt.key
                        node.left = self._delete_max(node.left) 
                    else:
                        # rgt = self.min_key_node(node.right) # можно убрать "костыль 2" если удалять прямо здесь (новую аналогичную функцию создать)
                        # node.key = rgt.key
                        # current_event = self.event[0] #костыль 2
                        # self.change_event(Vector(rgt.key.get_X(self.event[0].y), self.event[0].y)) #костыль 2
                        # node.right = self.node_delete(node.right, rgt)
                        # self.change_event(current_event) #костыль 2
                        rgt = self.min_key_node(node.right)
                        node.key = rgt.key
                        node.right = self._delete_min(node.right)

        if node is None:
            return node
        self._correction_height(node)
        return self.balancing_node(node)

    def inorder_print(self):
        err = False
        nodes = self.inorder()
        if nodes:
            lp = nodes[0].key.get_X(self.event[0].y)
            print(lp, nodes[0])
            for node in nodes:
                if node != nodes[0]:
                    np = node.key.get_X(self.event[0].y)
                    if (np-lp < 0) and (abs(np-lp) > 10**(2-_NDIGITS)):
                        err = True
                    print(np, node)
                    lp = np
            if err:
                raise Exception("Ошибка в поиске " + str(self.event[0].x))
        return


def _Error3(status: AVL_sweep_line, q):
    print(q[1],":", "segment:", q[2].begin, q[2].end)
    if q[1]==3:
        print("  :", "segment:", q[3].begin, q[3].end,'\n')
    print("координата скана:", q[0].y)
    status.inorder_print()
    raise Exception("Ошибка в поиске "+str(q[0].x))


def sweep_line(array_segments: list[Segment]):
    unprocessed_events = []
    intersecting_segments = set()
    intersection_points_with_dublicate = []

    def append_point(q_y, segment1: Segment, segment2: Segment):
        """Добавляю событие пересечения отрезков в unprocessed_events, если они пересекаются"""
        p1 = str(segment1.id)+" "+str(segment2.id)
        p2 = str(segment2.id)+" "+str(segment1.id)
        point = segment1.intersection_with_segments(segment2)
        if not (point is None):
            if q_y<=point.y and not (p1 in intersecting_segments) and not (p2 in intersecting_segments): # <= и не в множестве intersection_points_with_dublicate
                hq.heappush(unprocessed_events, (point, 3, segment1, segment2))
                hq.heappush(intersection_points_with_dublicate, (point, segment1, segment2))
                intersecting_segments.add(p1)
                intersecting_segments.add(p2)
                # print(point)
        return

    for segment in array_segments:
        hq.heappush(unprocessed_events, (segment.begin, 1, segment))
        hq.heappush(unprocessed_events, (segment.end, 2, segment))
    status = AVL_sweep_line()
    while unprocessed_events:
        q = hq.heappop(unprocessed_events)       
        # сдвиг сканирующей точки
        status.change_event(q[0])
        if q[1] == 1:
            # добавить отрезок в status
            status.insert(q[2])
            # проверить его на пересечения с соседями (х2)
            neighbors = status.get_nearests(q[2])
            if not (neighbors[0] is None):
                append_point(q[0].y, q[2], neighbors[0].key)
            if not (neighbors[1] is None):
                append_point(q[0].y, q[2], neighbors[1].key)

        elif q[1] == 2:
            # проверить на пересечение новообразовавшихся соседей (х1)
            neighbors = status.get_nearests(q[2])
            if not ((neighbors[0] is None) or (neighbors[1] is None)):
                append_point(q[0].y, neighbors[0].key, neighbors[1].key)
            # удалить отрезок из status
            status.delete(q[2])

        elif q[1] == 3:  #(point, 3, segment1, segment2)
            # проверить на пересечение новообразовавшихся соседей (х2)
            node1 = status.find(q[2])
            neighbors1 = status.get_nearests(q[2])
            node2 = status.find(q[3])
            neighbors2 = status.get_nearests(q[3])

            if (node1 is None) or (node2 is None):
                _Error3(status, q)
            
            if not (neighbors1[0] is None):
                if (neighbors1[0] != node2):
                    append_point(q[0].y, neighbors1[0].key, node2.key)
                else:
                    if not (neighbors1[1] is None):
                        append_point(q[0].y, neighbors1[1].key, node2.key)
            
            if not (neighbors2[0] is None):
                if (neighbors2[0] != node1):
                    append_point(q[0].y, neighbors2[0].key, node1.key)
                else:
                    if not (neighbors2[1] is None):
                        append_point(q[0].y, neighbors2[1].key, node1.key)
            # поменять местами пересекающиеся отрезки
            status.swap(node1, node2)
    #     print(q[1])
    #     status.inorder_print()
    #     print('------------=================------------')
    # status.inorder_print()
    return intersection_points_with_dublicate


def draw_lines(array_segments: list[Segment], intersection_points: list):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    if intersection_points:
        x_values = []
        y_values = []
        for point in intersection_points:
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
        array_segments.append(Segment(p1, p2, i))
    return array_segments


def main():
    array_segments = rundom_segments(400)
    draw_lines(array_segments, [])
    intersection_points = sweep_line(array_segments)
    print(len(intersection_points))
    draw_lines(array_segments, intersection_points)

if __name__ == '__main__':
    main()

    # a0 = Vector(0, 0)
    # b0 = Vector(1, 0)
    # c0 = Vector(2, 0)
    # a1 = Vector(0, 1)
    # b1 = Vector(1, 1)
    # c1 = Vector(2, 1)
    # s1 = Segment(a0, c1, 1)
    # s2 = Segment(b0, b1, 2)
    # s3 = Segment(c0, a1, 3)
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

    # intersections = sweep_line(segments)
    # print(len(intersections))
    # draw_lines(segments, intersections)

    # print(s1, s2, s3)
    # print(b1, s1.distance_point_from_segment(b1))
    # print(b0, s1.distance_point_from_segment(b0))
    # print(p, s1.distance_point_from_segment(p))

    # Tree = AVL_sweep_line()
    # for s in segments:
    #     Tree.change_event(s.begin)
    #     Tree.insert(s)
    # Tree.print2()
    # Tree.inorder_print()
    # print(Tree.find(s1))
    # print(Tree.find(s2))
    # print(Tree.find(s3))
    # Tree.delete(s2)
    # Tree.print2()
    # Tree.inorder_print()
    # draw_lines(segments, intersection_points)
    
    # segments = [s1, s2]

    
    # from math import sqrt
    # a = Vector(sqrt(2), 0.156)
    # b = Vector(1, 0)
    # s1 = Segment(a, b)
    # print(s1.get_X(0.1155))

