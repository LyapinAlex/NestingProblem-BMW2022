class node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVL:

    def height(self, Node):
        if Node is None:
            return 0
        else:
            return Node.height

    def balance(self, Node):
        if Node is None:
            return 0
        else:
            return self.height(Node.left) - self.height(Node.right)

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
        Node.height = 1 + max(self.height(Node.left), self.height(Node.right))
        a.height = 1 + max(self.height(a.left), self.height(a.right))
        return a

    def rotateL(self, Node):
        a = Node.right
        b = a.left
        a.left = Node
        Node.right = b
        Node.height = 1 + max(self.height(Node.left), self.height(Node.right))
        a.height = 1 + max(self.height(a.left), self.height(a.right))
        return a

    def insert(self, key_val, val, root):
        if root is None:
            return node(key_val, val)
        elif key_val <= root.key:
            root.left = self.insert(key_val, val, root.left)
        elif key_val > root.key:
            root.right = self.insert(key_val, val, root.right)
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.balance(root)
        if balance > 1 and root.left.key > key_val:
            return self.rotateR(root)
        if balance < -1 and key_val > root.right.key:
            return self.rotateL(root)
        if balance > 1 and key_val > root.left.key:
            root.left = self.rotateL(root.left)
            return self.rotateR(root)
        if balance < -1 and key_val < root.right.key:
            root.right = self.rotateR(root.right)
            return self.rotateL(root)
        return root

    def find(self, key, root):
        if root is None:
            return
        if root.key<key:
            return self.find(key, root.right)
        elif root.key>key:
            return self.find(key, root.left)
        else:
            return root.key, root.value

    def delete(self, key_val, Node):
        if Node is None:
            return Node
        elif key_val < Node.key:
            Node.left = self.delete(key_val, Node.left)
        elif key_val > Node.key:
            Node.right = self.delete(key_val, Node.right)
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
            Node.right = self.delete(rgt.key, Node.right)
        if Node is None:
            return Node
        Node.height = 1 + max(self.height(Node.left), self.height(Node.right))
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

    def preorder(self, root):
        res = []
        if root is None:
            return []
        res.append(root.key)
        res = res + self.preorder(root.left)
        res = res + self.preorder(root.right)
        return res

    def inorder(self, root):
        res = []
        if root is None:
            return []
        res = self.inorder(root.left)
        res.append(root.key)
        res = res + self.inorder(root.right)
        return res

Tree = AVL()
rt = None
rt = Tree.insert(3, 4, rt)
rt = Tree.insert(5, 6, rt)
rt = Tree.insert(7, 8, rt)
print("PREORDER: ", Tree.preorder(rt))
rt = Tree.insert(1, 2, rt)
rt = Tree.insert(2, 3, rt)
print("PREORDER: ", Tree.preorder(rt))
rt = Tree.insert(4, 5, rt)
rt = Tree.insert(6, 7, rt)
rt = Tree.delete(7, rt)
rt = Tree.insert(8, 9, rt)
rt = Tree.insert(9, 10, rt)
print("PREORDER: ", Tree.preorder(rt))
rt = Tree.delete(3, rt)
print(Tree.find(4,rt))
print("PREORDER: ", Tree.preorder(rt))
print("INORDER: ", Tree.inorder(rt))