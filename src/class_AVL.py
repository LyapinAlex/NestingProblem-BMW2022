class node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self):
        self.root = None

    def height(self):
        return self.node_height(self.root)

    def node_height(self, Node):
        if Node is None:
            return 0
        else:
            return Node.height

    def balance(self, Node):
        if Node is None:
            return 0
        else:
            return self.node_height(Node.left) - self.node_height(Node.right)

    def MinimumKeyNode(self, Node):
        if Node is None or Node.left is None:
            return Node
        else:
            return self.MinimumKeyNode(Node.left)

    def rotateR(self, Node):
        a = Node.left
        b = a.right
        a.right = Node
        Node.left = b
        Node.height = 1 + max(self.node_height(Node.left), self.node_height(Node.right))
        a.height = 1 + max(self.node_height(a.left), self.node_height(a.right))
        return a

    def rotateL(self, Node):
        a = Node.right
        b = a.left
        a.left = Node
        Node.right = b
        Node.height = 1 + max(self.node_height(Node.left), self.node_height(Node.right))
        a.height = 1 + max(self.node_height(a.left), self.node_height(a.right))
        return a

    def insert(self, key_val, val):
        a = self.node_insert(key_val, val, self.root)
        self.root = a

    def node_insert(self, key_val, val, Node):
        if Node is None:
            return node(key_val, val)
        elif key_val <= Node.key:
            Node.left = self.node_insert(key_val, val, Node.left)
        elif key_val > Node.key:
            Node.right = self.node_insert(key_val, val, Node.right)
        Node.height = 1 + max(self.node_height(Node.left), self.node_height(Node.right))
        balance = self.balance(Node)
        if balance > 1 and Node.left.key > key_val:
            return self.rotateR(Node)
        if balance < -1 and key_val > Node.right.key:
            return self.rotateL(Node)
        if balance > 1 and key_val > Node.left.key:
            Node.left = self.rotateL(Node.left)
            return self.rotateR(Node)
        if balance < -1 and key_val < Node.right.key:
            Node.right = self.rotateR(Node.right)
            return self.rotateL(Node)
        return Node

    def find(self, key):
        return self.node_find(key, self.root)

    def node_find(self, key, Node):
        if Node is None:
            return
        if Node.key<key:
            return self.node_find(key, Node.right)
        elif Node.key>key:
            return self.node_find(key, Node.left)
        else:
            return Node.key, Node.value

    def delete(self, key_val):
        a = self.node_delete(key_val, self.root)
        self.root = a

    def node_delete(self, key_val, Node):
        if Node is None:
            return Node
        elif key_val < Node.key:
            Node.left = self.node_delete(key_val, Node.left)
        elif key_val > Node.key:
            Node.right = self.node_delete(key_val, Node.right)
        else:
            if Node.left is None:
                lt = Node.right
                Node = None
                return lt
            elif Node.right is None:
                lt = Node.left
                Node = None
                return lt
            rgt = self.MinimumKeyNode(Node.right)
            Node.key = rgt.key
            Node.value = rgt.value
            Node.right = self.node_delete(rgt.key, Node.right)
        if Node is None:
            return Node
        Node.height = 1 + max(self.node_height(Node.left), self.node_height(Node.right))
        balance = self.balance(Node)
        if balance > 1 and self.balance(Node.left) >= 0:
            return self.rotateR(Node)
        if balance < -1 and self.balance(Node.right) <= 0:
            return self.rotateL(Node)
        if balance > 1 and self.balance(Node.left) < 0:
            Node.left = self.rotateL(Node.left)
            return self.rotateR(Node)
        if balance < -1 and self.balance(Node.right) > 0:
            Node.right = self.rotateR(Node.right)
            return self.rotateL(Node)
        return Node

    def preorder(self):
        return self.node_preorder(self.root)

    def node_preorder(self, Node):
        res = []
        if Node is None:
            return []
        res.append(Node.key)
        res = res + self.node_preorder(Node.left)
        res = res + self.node_preorder(Node.right)
        return res

    def inorder(self):
        return self.node_inorder(self.root)

    def node_inorder(self, Node):
        res = []
        if Node is None:
            return []
        res = self.node_inorder(Node.left)
        res.append(Node.key)
        res = res + self.node_inorder(Node.right)
        return res

Tree = AVL()
Tree.insert(3,4)
Tree.insert(5,6)
Tree.insert(7,8)
print("PREORDER: ", Tree.preorder())
Tree.insert(1,2)
Tree.insert(2,3)
print("PREORDER: ", Tree.preorder())
Tree.insert(4,5)
Tree.insert(6,7)
Tree.delete(7)
Tree.insert(8,9)
Tree.insert(9,10)
print("PREORDER: ", Tree.preorder())
Tree.delete(3)
print(Tree.find(4))
print("PREORDER: ", Tree.preorder())
print("INORDER: ", Tree.inorder())
print(Tree.height())
