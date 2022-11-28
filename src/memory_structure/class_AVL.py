class Node:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

    def __str__(self):  # print
        return 'K: {}, V:{}'.format(self.key, self.value)

    def __eq__(self, other): # ==
        return self.key == other.key

    def __lt__(self, other):  # <
        return self.key < other.key

    def __gt__(self, other):  # >
        return self.key > other.key

    def __le__(self, other):  # <=
        return self == other or self < other

    def __ge__(self, other):  # >=
        return self == other or self > other



class AVL:
    #! есть вероятность, что одинаковые ключи сломают структуру через балансировку
    def __init__(self):
        self.root = None

    def create_node(self, key, value):
        return Node(key, value)

    # ----------------------------  structure information  ----------------------------

    def height(self):
        return self.node_height(self.root)

    def node_height(self, node):
        if node is None:
            return 0
        else:
            return node.height

    def _balance(self, node):
        if node is None:
            return 0
        else:
            return self.node_height(node.left) - self.node_height(node.right)

    def _correction_height(self, node):
        node.height = 1 + max(self.node_height(node.left),
                              self.node_height(node.right))
        return node.height

    # ----------------------------  extracting nodes  ----------------------------

    def min_key_node(self, node):
        if node is None or node.left is None:
            return node
        else:
            return self.min_key_node(node.left)

    def max_key_node(self, node):
        if node is None or node.right is None:
            return node
        else:
            return self.max_key_node(node.right)

    def find(self, key, value=None):
        searchable_node = self.create_node(key, value)
        return self.node_find(self.root, searchable_node)

    def node_find(self, node, searchable_node):
        if node is None:
            return
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

    def get_nearests(self, key, value=None):
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

    # ----------------------------  change the tree structure  ----------------------------

    def _small_rotate_R(self, node):
        a = node.left
        node.left = a.right
        a.right = node
        self._correction_height(node)
        self._correction_height(a)
        return a

    def _big_rotate_R(self, node):
        node.left = self._small_rotate_L(node.left)
        return self._small_rotate_R(node)

    def _small_rotate_L(self, node):
        a = node.right
        node.right = a.left
        a.left = node
        self._correction_height(node)
        self._correction_height(a)
        return a

    def _big_rotate_L(self, node):
        node.right = self._small_rotate_R(node.right)
        return self._small_rotate_L(node)

    def balancing_node(self, node):
        balance = self._balance(node)

        balanceR = self._balance(node.right)
        if balance == -2 and (balanceR == 0 or balanceR == -1):
            return self._small_rotate_L(node)
        if balance == -2 and balanceR == 1:
            return self._big_rotate_L(node)

        balanceL = self._balance(node.left)
        if balance == 2 and (balanceL == 0 or balanceL == 1):
            return self._small_rotate_R(node)
        if balance == 2 and balanceL == -1:
            return self._big_rotate_R(node)

        return node

    # ----------------------------  change the content  ----------------------------

    def insert(self, key_val, val):
        implemented_node = self.create_node(key_val, val)
        a = self.node_insert(self.root, implemented_node)
        self.root = a

    def node_insert(self, node, implemented_node):
        if node is None:
            return implemented_node
        elif implemented_node <= node:
            node.left = self.node_insert(node.left, implemented_node)
        elif implemented_node > node:
            node.right = self.node_insert(node.right, implemented_node)
        self._correction_height(node)
        return self.balancing_node(node)

    def delete(self, key_val, value=None):
        """По ключу удаляет первую встречную в дереве вершину с данным ключом\\
        по ключу и значению удаляет все вершины с данными ключом и значением\\
        если не находит что удалить, то ничего не делает"""
        excluded_node = self.create_node(key_val, value)
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

    # ----------------------------  other representations  ----------------------------

    def node_preorder(self, node):
        res = []
        if node is None:
            return []
        res.append(node)
        res = res + self.node_preorder(node.left)
        res = res + self.node_preorder(node.right)
        return res

    def preorder(self):
        return self.node_preorder(self.root)

    def node_inorder(self, node):
        res = []
        if node is None:
            return []
        res = self.node_inorder(node.left)
        res.append(node)
        res = res + self.node_inorder(node.right)
        return res

    def inorder(self):
        """Возвращает список узлов в возростающем порядке"""
        return self.node_inorder(self.root)

    def inorder_print(self):
        nodes = self.inorder()
        for node in nodes:
            print(node)
        return
    
    def print2(self):
        print("      ", self.root)
        print(self.root.left, self.root.right)
        return

if __name__ == '__main__':
    Tree = AVL()

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

    Tree.delete(4)

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
    Tree.delete(27)
    Tree.delete(8,1)
    Tree.delete(14)
    print("-------------------=====================-------------------")
    Tree.inorder_print()
    print("-------------------=====================-------------------")
