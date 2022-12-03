class Node:

    def __init__(self, key, value=None):  # NEED VALUE
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

    def __str__(self):  # print
        return 'K: {}'.format(self.key)

    def __repr__(self):
        return 'Node({})'.format(self.key)

    # ----------------------------  Logical operations   ----------------------------

    def __eq__(self, other):  # == ALL OKAY, JUST PEREGRUZIT' OPERATORS IN DAUGHTER CLASS
        return self.key == other.key

    def __lt__(self, other):  # <
        return self.key < other.key

    def __gt__(self, other):  # >
        return self.key > other.key

    def __ne__(self, other):  # !=
        return not (self == other)

    def __le__(self, other):  # <=
        return self == other or self < other

    def __ge__(self, other):  # >=
        return self == other or self > other

    def swap_data(self, other):  # MAYBE NOT OK
        tmp_key = other.key
        tmp_value = other.value
        other.key = self.key
        other.value = self.value
        self.key = tmp_key
        self.value = tmp_value


class AvlTree:
    #! есть вероятность, что одинаковые ключи "сломают" структуру через балансировку
    def __init__(self):
        self.root = None

    def __repr__(self):
        return 'AVL({})'.format(self.root)

    def create_node(self, key):  # NOT OK
        return Node(key)

    def swap(self, node1, node2):  # NOT OK!!!!!!!!!!!!
        """Меняет местами ключи и значения"""
        node1.swap_data(node2)

    # ----------------------------  structure information  ----------------------------

    def height(self):  # OK
        return self.node_height(self.root)

    def node_height(self, node):  # OK
        if node is None:
            return 0
        else:
            return node.height

    def _balance(self, node):  # Ok
        if node is None:
            return 0
        else:
            return self.node_height(node.left) - self.node_height(node.right)

    def _correction_height(self, node):  # OK
        node.height = 1 + max(self.node_height(node.left),
                              self.node_height(node.right))
        return node.height

    # ----------------------------  extracting nodes  ----------------------------

    def min_key_node(self, node):  # OK
        if node is None or node.left is None:
            return node
        else:
            return self.min_key_node(node.left)

    def max_key_node(self, node):  # OK
        if node is None or node.right is None:
            return node
        else:
            return self.max_key_node(node.right)

    def find(self, key):
        searchable_node = self.create_node(key)  # Maybe OK!
        return self.node_find(self.root, searchable_node)

    def node_find(self, node, searchable_node):  # Maybe OK
        if node is None:
            return
        if searchable_node > node:
            return self.node_find(node.right, searchable_node)
        elif searchable_node < node:
            return self.node_find(node.left, searchable_node)
        else:
            # if (node.key == searchable_node.key):
            #     return node
            # else:
            # ans1 = self.node_find(node.left, searchable_node)
            # if ans1 is None:
            #     ans1 = self.node_find(node.right, searchable_node)
            # return ans1
            return node

    def get_nearests(self, key):  # NOT OK!
        """Ищет пару чисел по ключу таких, что \\
        первое - минимальное среди тех кто больше (если нет то None) \\
        второе - максимальное среди тех кто меньше (если нет то None)"""
        node_key = self.find(key)
        neighbors = [None, None]
        if not (node_key is None):
            neighbors[0] = self.min_key_node(node_key.right)
            neighbors[1] = self.max_key_node(node_key.left)

        if (neighbors[0] is None) or (neighbors[1] is None):
            searchable_node = self.create_node(key)  # NOT OK!
            turnsLR = self._find_last_turnsLR(self.root, searchable_node)
            if neighbors[0] is None:
                neighbors[0] = turnsLR[0]
            if neighbors[1] is None:
                neighbors[1] = turnsLR[1]
        return neighbors

    def _find_last_turnsLR(self, node, searchable_node):  # OK
        turnsLR = [None, None]
        if node is None:
            return turnsLR
        if searchable_node > node:
            turnsLR = self._find_last_turnsLR(node.right, searchable_node)
            if turnsLR[1] is None:
                turnsLR[1] = node
        elif searchable_node < node:
            turnsLR = self._find_last_turnsLR(node.left, searchable_node)
            if turnsLR[0] is None:
                turnsLR[0] = node
        return turnsLR
        # if node.key == searchable_node.key:
        #     return turnsLR
        # else:
        #     if self.node_find(node.right, searchable_node) is None:
        #         turnsLR = self._find_last_turnsLR(node.left, searchable_node)
        #         if turnsLR[0] is None:
        #             turnsLR[0] = node
        #     else:
        #         turnsLR = self._find_last_turnsLR(node.right, searchable_node)
        #         if turnsLR[1] is None:
        #             turnsLR[1] = node
        #     return turnsLR

    # ----------------------------  change the tree structure  ----------------------------

    def _small_rotate_R(self, node):  # OK
        a = node.left
        node.left = a.right
        a.right = node
        self._correction_height(node)
        self._correction_height(a)
        return a

    def _big_rotate_R(self, node):  # OK
        node.left = self._small_rotate_L(node.left)
        return self._small_rotate_R(node)

    def _small_rotate_L(self, node):  # OK
        a = node.right
        node.right = a.left
        a.left = node
        self._correction_height(node)
        self._correction_height(a)
        return a

    def _big_rotate_L(self, node):  # OK
        node.right = self._small_rotate_R(node.right)
        return self._small_rotate_L(node)

    def balancing_node(self, node):  # OK
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

    def insert(self, implemented_node):  # OK
        a = self.node_insert(self.root, implemented_node)
        self.root = a

    def node_insert(self, node, implemented_node):  # OK
        if node is None:
            return implemented_node
        elif implemented_node > node:
            node.right = self.node_insert(node.right, implemented_node)
        else:
            node.left = self.node_insert(node.left, implemented_node)
        self._correction_height(node)
        return self.balancing_node(node)

    def delete(self, key):  # NOT OK!!!!!!!!!!!!!!!!!!!!!
        """По ключу удаляет первую встречную в дереве вершину с данным ключом\\
        если не находит что удалить, то ничего не делает"""
        excluded_node = self.create_node(key)
        a = self.node_delete(self.root, excluded_node)
        self.root = a

    # NOT OK!!!!!!!!!!!!!!!!!!!1!!!!!!!!!!!!
    def node_delete(self, node: 'Node', excluded_node):
        if node is None:
            return node
        elif excluded_node < node:
            node.left = self.node_delete(node.left, excluded_node)
        elif excluded_node > node:
            node.right = self.node_delete(node.right, excluded_node)
        else:
            if (node.left is None) and (node.right is None):
                node = None
            else:
                if self._balance(node) > 0:
                    rgt = self.max_key_node(node.left)
                    node.swap_data(rgt)
                    node.left = self._delete_max(node.left)
                else:
                    rgt = self.min_key_node(node.right)
                    node.swap_data(rgt)
                    node.right = self._delete_min(node.right)
        if node is None:
            return node
        self._correction_height(node)
        return self.balancing_node(node)

    def _delete_min(self, node):  # NOT OK!!!!!!!!!!!!!!!!!!!!!1
        if (node.left is None) and (node.right is None):
            return None
        if not (node.left is None):
            node.left = self._delete_min(node.left)
        else:
            node.swap_data(node.right)
            node.right = None

        if node is None:
            return node
        self._correction_height(node)
        return self.balancing_node(node)

    def _delete_max(self, node):  # NOT OK!!!!!!!!!!!!!!!
        if (node.left is None) and (node.right is None):
            return None
        if not (node.right is None):
            node.right = self._delete_max(node.right)
        else:
            node.swap_data(node.left)
            node.left = None

        if node is None:
            return node
        self._correction_height(node)
        return self.balancing_node(node)

    # ----------------------------  other representations  ----------------------------

    def node_preorder(self, node):  # OK
        res = []
        if node is None:
            return []
        res.append(node)
        res = res + self.node_preorder(node.left)
        res = res + self.node_preorder(node.right)
        return res

    def preorder(self):  # OK
        return self.node_preorder(self.root)

    def node_inorder(self, node):  # OK
        res = []
        if node is None:
            return []
        res = self.node_inorder(node.left)
        res.append(node)
        res = res + self.node_inorder(node.right)
        return res

    def inorder(self):  # OK
        """Возвращает список узлов в возростающем порядке"""
        return self.node_inorder(self.root)

    def inorder_print(self):  # OK
        nodes = self.inorder()
        for node in nodes:
            print(node)
        return

    def print2(self):  # OK
        print("      ", self.root)
        print(self.root.left, self.root.right)
        return


if __name__ == '__main__':
    Tree = AvlTree()

    Tree.insert(Node(11))
    Tree.insert(Node(1))
    Tree.insert(Node(4))
    Tree.insert(Node(5))
    Tree.insert(Node(14))
    Tree.insert(Node(6))
    Tree.insert(Node(9))
    Tree.insert(Node(8))
    Tree.insert(Node(10))
    Tree.insert(Node(13))
    Tree.insert(Node(2))
    Tree.insert(Node(3))
    Tree.insert(Node(12))
    Tree.insert(Node(15))
    Tree.insert(Node(7))

    print("-------------------=====================-------------------")
    print()

    print("                   ", Tree.root)
    print("               ", Tree.root.left, Tree.root.right)
    print("         ", Tree.root.left.left, Tree.root.left.right,
          Tree.root.right.left, Tree.root.right.right)
    print(Tree.root.left.left.left, Tree.root.left.left.right,
          Tree.root.left.right.left, Tree.root.left.right.right,
          Tree.root.right.left.left, Tree.root.right.left.right,
          Tree.root.right.right.left, Tree.root.right.right.right)

    print()
    print("-------------------=====================-------------------")

    Tree.delete(2)

    print("-------------------=====================-------------------")
    print()

    print("                   ", Tree.root)
    print("               ", Tree.root.left, Tree.root.right)
    print("         ", Tree.root.left.left, Tree.root.left.right,
          Tree.root.right.left, Tree.root.right.right)
    print(Tree.root.left.left.left, Tree.root.left.left.right,
          Tree.root.left.right.left, Tree.root.left.right.right,
          Tree.root.right.left.left, Tree.root.right.left.right,
          Tree.root.right.right.left, Tree.root.right.right.right)

    print()
    print("-------------------=====================-------------------")
    Tree.inorder_print()
