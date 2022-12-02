class Node:

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

    def __str__(self):  # print
        return 'K: {}'.format(self.key)

    def __repr__(self):
        return 'Node({})'.format(self.key)

    def swap_data(self, other: 'Node'):
        key = self.key
        self.key = other.key
        other.key = key

    # ----------------------------  Logical operations   ----------------------------

    def __eq__(self, other: 'Node') -> bool:  # ==
        return self.key == other.key

    def __lt__(self, other: 'Node') -> bool:  # <
        return self.key < other.key

    def __gt__(self, other: 'Node') -> bool:  # >
        return self.key > other.key

    def __ne__(self, other: 'Node') -> bool:  # !=
        return not (self == other)

    def __le__(self, other: 'Node') -> bool:  # <=
        return self == other or self < other

    def __ge__(self, other: 'Node') -> bool:  # >=
        return self == other or self > other


class AVL:
    #! есть вероятность, что одинаковые ключи "сломают" структуру через балансировку
    def __init__(self):
        self.root = None

    def __repr__(self):
        return 'AVL({})'.format(self.root)

    def create_node(self, key) -> Node:
        return Node(key)

    def swap(self, node1: Node, node2: Node):
        """Меняет местами только ключи"""
        key = node1.key
        node1.key = node2.key
        node2.key = key

    # ----------------------------  structure information  ----------------------------

    def height(self) -> int:
        """Возвращает высоту дерева"""
        return self.node_height(self.root)

    def node_height(self, node: Node) -> int:
        if node is None:
            return 0
        else:
            return node.height

    def _balance(self, node: Node) -> int:
        if node is None:
            return 0
        else:
            return self.node_height(node.left) - self.node_height(node.right)

    def _correction_height(self, node: Node) -> int:
        node.height = 1 + max(self.node_height(node.left),
                              self.node_height(node.right))
        return node.height

    # ----------------------------  extracting nodes  ----------------------------

    def min_key_node(self, node: Node) -> Node:
        """Возвращает \"минимальный\" узел в поддереве, корень которого node (если такого нет, то None)"""
        if node is None or node.left is None:
            return node
        else:
            return self.min_key_node(node.left)

    def max_key_node(self, node: Node) -> Node:
        """Возвращает \"максимальный\" узел в поддереве, корень которого node (если такого нет, то None)"""
        if node is None or node.right is None:
            return node
        else:
            return self.max_key_node(node.right)

    def find(self, key) -> Node:
        """По ключу ищет узел в дереве"""
        searchable_node = self.create_node(key)
        return self.node_find(self.root, searchable_node)

    def node_find(self, node: Node, searchable_node: Node) -> Node:
        """По узлу ищет узел в поддереве, корнем которого является node"""
        if node is None:
            return
        if searchable_node > node:
            return self.node_find(node.right, searchable_node)
        elif searchable_node < node:
            return self.node_find(node.left, searchable_node)
        else:
            return node

    def get_nearests(self, key) -> list[Node]:
        """Ищет пару чисел по ключу таких, что \\ 
        первое - минимальное среди тех кто больше (соседа который больше), если нет то None \\
        второе - максимальное среди тех кто меньше (соседа который меньше), если нет то None"""
        node_key = self.find(key)
        neighbors = [None, None]
        if not (node_key is None):
            neighbors[0] = self.min_key_node(node_key.right)
            neighbors[1] = self.max_key_node(node_key.left)

        if (neighbors[0] is None) or (neighbors[1] is None):
            searchable_node = self.create_node(key)
            turnsLR = self._find_last_turnsLR(self.root, searchable_node)
            if neighbors[0] is None:
                neighbors[0] = turnsLR[0]
            if neighbors[1] is None:
                neighbors[1] = turnsLR[1]
        return neighbors

    def _find_last_turnsLR(self, node: Node,
                           searchable_node: Node) -> list[Node]:
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

    # ----------------------------  change the tree structure  ----------------------------

    def _small_rotate_R(self, node: Node) -> Node:
        a = node.left
        node.left = a.right
        a.right = node
        self._correction_height(node)
        self._correction_height(a)
        return a

    def _big_rotate_R(self, node: Node) -> Node:
        node.left = self._small_rotate_L(node.left)
        return self._small_rotate_R(node)

    def _small_rotate_L(self, node: Node) -> Node:
        a = node.right
        node.right = a.left
        a.left = node
        self._correction_height(node)
        self._correction_height(a)
        return a

    def _big_rotate_L(self, node: Node) -> Node:
        node.right = self._small_rotate_R(node.right)
        return self._small_rotate_L(node)

    def balancing_node(self, node: Node) -> Node:
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

    def insert(self, key):
        """Производит вставку элемента в дерево"""
        implemented_node = self.create_node(key)
        a = self.node_insert(self.root, implemented_node)
        self.root = a

    def node_insert(self, node: Node, implemented_node: Node) -> Node:
        """Производит вставку узла в поддерево с корнем node"""
        if node is None:
            return implemented_node
        elif implemented_node > node:
            node.right = self.node_insert(node.right, implemented_node)
        else:
            node.left = self.node_insert(node.left, implemented_node)
        self._correction_height(node)
        return self.balancing_node(node)

    def delete(self, key):
        """По ключу удаляет первую встречную в дереве вершину с данным ключом\\
        если не находит что удалить, то ничего не делает"""
        excluded_node = self.create_node(key)
        a = self.node_delete(self.root, excluded_node)
        self.root = a

    def node_delete(self, node: Node, excluded_node: Node) -> Node:
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

    def _delete_min(self, node: Node) -> Node:
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

    def _delete_max(self, node: Node) -> Node:
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

    def node_preorder(self, node: Node) -> list[Node]:
        res = []
        if node is None:
            return []
        res.append(node)
        res = res + self.node_preorder(node.left)
        res = res + self.node_preorder(node.right)
        return res

    def preorder(self) -> list[Node]:
        return self.node_preorder(self.root)

    def node_inorder(self, node: Node) -> list[Node]:
        res = []
        if node is None:
            return []
        res = self.node_inorder(node.left)
        res.append(node)
        res = res + self.node_inorder(node.right)
        return res

    def inorder(self) -> list[Node]:
        """Возвращает список узлов в возростающем порядке"""
        return self.node_inorder(self.root)

    def inorder_print(self):
        """Вывод дерева в возростающем порядке"""
        nodes = self.inorder()
        for node in nodes:
            print(node)



if __name__ == '__main__':
    Tree = AVL()

    Tree.insert(11)
    Tree.insert(1)
    Tree.insert(4)
    Tree.insert(5)
    Tree.insert(14)
    Tree.insert(6)
    Tree.insert(9)
    Tree.insert(8)
    Tree.insert(10)
    Tree.insert(13)
    Tree.insert(2)
    Tree.insert(3)
    Tree.insert(12)
    Tree.insert(15)
    Tree.insert(7)

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

    Tree.delete(9)
    Tree.delete(2)
    Tree.delete(1)
    Tree.delete(14)

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

    print(Tree.get_nearests(8))