from typing import Any, NoReturn

RED, BLACK = "RED", "BLACK"


class Node:
    def __init__(self, color: str, key: int, value: Any = None, left=None, right=None, parent=None):
        self.color = color
        self.key = key
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right

    def __str__(self) -> str:
        left = self.left.key if self.left else "nil"
        right = self.right.key if self.right else "nil"
        parent = self.parent.key if self.parent else None
        return f"(|{self.color}| - key:{self.key}, value:{self.key}): left: {left}, right: {right}, parent: {parent}"


class RBTree:

    def __init__(self):
        self.__nil = Node(BLACK, -1)
        self.__root = self.__nil

    def __setitem__(self, key: int, value: Any) -> NoReturn:
        node_new = Node(RED, key, value, self.__nil, self.__nil, None)
        if self.__root == self.__nil:
            self.__root = node_new
            return
        node = None
        current = self.__root

        while current != self.__nil:
            node = current
            if node_new.key < current.key:
                current = current.left
            else:
                current = current.right

        node_new.parent = node
        if node_new.key < node.key:
            node.left = node_new
        else:
            node.right = node_new

        if node_new.parent is None:
            node_new.color = BLACK
            return

        if node_new.parent.parent is None:
            return

        self.__fix_node_insert(node_new)

    def __fix_node_insert(self, node: Node) -> NoReturn:
        while node.parent.color == RED:
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left
                if uncle.color == RED:
                    uncle.color = BLACK
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.__right_rotate(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self.__left_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.right
                if uncle.color == RED:
                    uncle.color = BLACK
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.__left_rotate(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self.__right_rotate(node.parent.parent)
            if node == self.__root:
                break
        self.__root.color = BLACK

    def __left_rotate(self, node: Node) -> NoReturn:
        tmp = node.right
        node.right = tmp.left
        if tmp.left != self.__nil:
            tmp.left.parent = node

        tmp.parent = node.parent
        if node.parent is None:
            self.__root = tmp
        elif node == node.parent.left:
            node.parent.left = tmp
        else:
            node.parent.right = tmp
        tmp.left = node
        node.parent = tmp

    def __right_rotate(self, node: Node) -> NoReturn:
        tmp = node.left
        node.left = tmp.right
        if tmp.right != self.__nil:
            tmp.right.parent = node

        tmp.parent = node.parent
        if node.parent is None:
            self.__root = tmp
        elif node == node.parent.right:
            node.parent.right = tmp
        else:
            node.parent.left = tmp
        tmp.right = node
        node.parent = tmp

    def remove(self, key: int) -> NoReturn:
        current = self.__root
        if current == self.__nil:
            return
        remove_node = None
        while current:
            if current.key == key:
                remove_node = current
                break
            if current.key <= key:
                current = current.right
            else:
                current = current.left
        if remove_node is None:
            return

        save_node = remove_node
        save_color = save_node.color

        if remove_node.left == self.__nil:
            child = remove_node.right
            self.__transplant(remove_node, remove_node.right)
        elif remove_node.right == self.__nil:
            child = remove_node.left
            self.__transplant(remove_node, remove_node.left)
        else:
            save_node = self.__minimum(remove_node.right)
            save_color = save_node.color
            child = save_node.right
            if child is None:
                child = self.__nil

            if save_node.parent == remove_node:
                child.parent = save_node
            else:
                self.__transplant(save_node, save_node.right)
                save_node.right = remove_node.right
                save_node.right.parent = save_node
            self.__transplant(remove_node, save_node)
            save_node.left = remove_node.left
            save_node.right.parent = save_node
            save_node.color = remove_node.color

        if save_color == BLACK:
            self.__fix_remove(child)

        if child.parent and child.parent.left == self.__nil:
            child.parent.left = None
        if child.parent and child.parent.right == self.__nil:
            child.parent.right = None
        self.__nil.parent = None

    def __transplant(self, node1, node2) -> NoReturn:
        if node1.parent is None:
            self.__root = node2
        elif node1 == node1.parent.left:
            node1.parent.left = node2
        else:
            node1.parent.right = node2
        node2 = self.__nil if node2 is None else node2
        node2.parent = node1.parent

    def __fix_remove(self, node: Node) -> NoReturn:
        if node == self.__nil:
            return
        while node != self.__root and node.color == BLACK:
            if node == node.parent.left:
                brother = node.parent.right
                if brother.color == RED:
                    brother.color = BLACK
                    node.parent.color = RED
                    self.__left_rotate(node.parent)
                    brother = node.parent.right
                if brother.left.color == BLACK and brother.right.color == BLACK:
                    brother.color = RED
                    node = node.parent
                else:
                    if brother.right.color == BLACK:
                        brother.left.color = BLACK
                        brother.color = RED
                        self.__right_rotate(brother)
                        brother = node.parent.right

                    brother.color = node.parent.color
                    node.parent.color = BLACK
                    brother.right.color = BLACK
                    self.__left_rotate(node.parent)
                    node = self.__root
            else:
                brother = node.parent.left
                if brother.color == RED:
                    brother.color = BLACK
                    node.parent.color = RED
                    self.__right_rotate(node.parent)
                    brother = node.parent.left
                if brother.right.color == BLACK and brother.right.color == BLACK:
                    brother.color = RED
                    node = node.parent
                else:
                    if brother.left.color == BLACK:
                        brother.right.color = BLACK
                        brother.color = RED
                        self.__left_rotate(brother)
                        brother = node.parent.left

                    brother.color = node.parent.color
                    node.parent.color = BLACK
                    brother.left.color = BLACK
                    self.__right_rotate(node.parent)
                    node = self.__root
        node.color = BLACK

    def __getitem__(self, key: int) -> Any:
        current = self.__root
        while current:
            if current.key == key:
                return current.value
            if current.key > key:
                current = current.left
            else:
                current = current.right

    def __minimum(self, node: Node) -> Node:
        if node is None:
            return self.__nil
        while node.left:
            node = node.left
        return node if node else self.__nil

    def print(self) -> NoReturn:
        self.__print_node(self.__root, "", True)

    def __print_node(self, node: Node, indent: str, last: bool) -> NoReturn:
        if node != self.__nil and node:
            print(indent, end=' ')
            if last:
                print("R----", end=' ')
                indent += "     "
            else:
                print("L----", end=' ')
                indent += " |    "

            print(node)
            self.__print_node(node.left, indent, False)
            self.__print_node(node.right, indent, True)
