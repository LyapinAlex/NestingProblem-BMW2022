if __name__ == '__main__':
    from class_AVL import AVL, Node
else:
    from .class_AVL import AVL, Node


class Node_KV(Node):

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

    def __str__(self):  # print
        return 'K: {}, V:{}'.format(self.key, self.value)

class AVL_KV(AVL):

    def create_node(self, key, value):
        return Node_KV(key, value)

    def swap(self, node1, node2):
        """Меняет местами только ключ и значение"""
        key = node1.key
        node1.key = node2.key
        node2.key = key
        value = node1.value
        node1.value = node2.value
        node2.value = value

    # ----------------------------  extracting nodes  ----------------------------

    def find(self, key, value):
        searchable_node = self.create_node(key, value)
        return self.node_find(self.root, searchable_node)

    def node_find(self, node, searchable_node):
        if node is None:
            return
        if searchable_node > node:
            return self.node_find(node.right, searchable_node)
        elif searchable_node < node:
            return self.node_find(node.left, searchable_node)
        else:
            if (node.value == searchable_node.value):
                return node
            else:
                ans1 = self.node_find(node.left, searchable_node)
                if ans1 is None:
                    ans1 = self.node_find(node.right, searchable_node)
                return ans1

    def get_nearests(self, key, value):
        """Ищет пару чисел по ключу таких, что \\ 
        первое - минимальное среди тех кто больше (если нет то None) \\
        второе - максимальное среди тех кто меньше (если нет то None)"""
        node_key = self.find(key, value)
        neighbors = [None, None]
        if not (node_key is None):
            neighbors[0] = self.min_key_node(node_key.right)
            neighbors[1] = self.max_key_node(node_key.left)

        if neighbors[0] is None or neighbors[1] is None:
            searchable_node = self.create_node(key, value)
            turnsLR = self._find_last_turnsLR(self.root, searchable_node)
            if neighbors[0] is None:
                neighbors[0] = turnsLR[0]
            if neighbors[1] is None:
                neighbors[1] = turnsLR[1]
        return neighbors

    def _find_last_turnsLR(self, node, searchable_node):
        turnsLR = [None, None]
        if node is None:
            return turnsLR
        if node < searchable_node:
            turnsLR = self._find_last_turnsLR(node.right, searchable_node)
            if turnsLR[1] is None:
                turnsLR[1] = node
        elif node > searchable_node:
            turnsLR = self._find_last_turnsLR(node.left, searchable_node)
            if turnsLR[0] is None:
                turnsLR[0] = node
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

    # ----------------------------  change the content  ----------------------------

    def insert(self, key, value):
        implemented_node = self.create_node(key, value)
        a = self.node_insert(self.root, implemented_node)
        self.root = a

    def delete(self, key, value):
        """По ключу и значению удаляет все вершины с данными ключом и значением\\
        если не находит что удалить, то ничего не делает"""
        excluded_node = self.create_node(key, value)
        a = self.node_delete(self.root, excluded_node)
        self.root = a

    def node_delete(self, node, excluded_node):
        if node is None:
            return node
        elif excluded_node < node:
            node.left = self.node_delete(node.left, excluded_node)
        elif excluded_node > node:
            node.right = self.node_delete(node.right, excluded_node)
        else:
            node.left = self.node_delete(node.left, excluded_node)
            node.right = self.node_delete(node.right, excluded_node)

            if (node.value == excluded_node.value):
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


if __name__ == '__main__':
    Tree = AVL_KV()

    Tree.insert(11, 0)
    Tree.insert(1, 0)
    Tree.insert(4, 0)
    Tree.insert(5, 0)
    Tree.insert(14, 0)
    Tree.insert(6, 0)
    Tree.insert(8, 1)
    Tree.insert(8, 2)
    Tree.insert(8, 1)
    Tree.insert(13, 0)
    Tree.insert(2, 0)
    Tree.insert(3, 0)
    Tree.insert(12, 0)
    Tree.insert(15, 0)
    Tree.insert(7, 0)

    print("                                  ", Tree.root)
    print("                            ", Tree.root.left, Tree.root.right)
    print("                  ", Tree.root.left.left, Tree.root.left.right,
          Tree.root.right.left, Tree.root.right.right)
    print(Tree.root.left.left.left, Tree.root.left.left.right,
          Tree.root.left.right.left, Tree.root.left.right.right,
          Tree.root.right.left.left, Tree.root.right.left.right,
          Tree.root.right.right.left, Tree.root.right.right.right)
    print()

    # neig = Tree.get_nearests(8)
    # print(neig[0], neig[1])
    # neig = Tree.get_nearests(8,0)
    # print(neig[0], neig[1])
    # neig = Tree.get_nearests(8,1)
    # print(neig[0], neig[1])
    # neig = Tree.get_nearests(8,2)
    # print(neig[0], neig[1])
    # print(Tree.find(8,2))

    Tree.delete(4, 0)

    print("                                  ", Tree.root)
    print("                            ", Tree.root.left, Tree.root.right)
    print("                  ", Tree.root.left.left, Tree.root.left.right,
          Tree.root.right.left, Tree.root.right.right)
    print(Tree.root.left.left.left, Tree.root.left.left.right,
          Tree.root.left.right.left, Tree.root.left.right.right,
          Tree.root.right.left.left, Tree.root.right.left.right,
          Tree.root.right.right.left, Tree.root.right.right.right)
    print()
    print("-------------------=====================-------------------")
    Tree.inorder_print()
    print("-------------------=====================-------------------")
    print(Tree.find(8, 1)==Tree.find(8, 2))
    print(Tree.get_nearests(8, 1)[1])
    Tree.delete(27, 5)
    Tree.delete(8,1)
    Tree.delete(14, 0)
    print("-------------------=====================-------------------")
    Tree.inorder_print()
    print("-------------------=====================-------------------")
