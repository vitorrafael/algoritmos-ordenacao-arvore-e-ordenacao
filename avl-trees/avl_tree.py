from node import Node


class AVLTree:
    def __init__(self) -> None:
        self.root: Node = None

    def insert_node(self, node_key: int) -> Node:
        node_to_be_inserted = Node(node_key)
        self.root = self.__insert_node(self.root, node_to_be_inserted)

    def remove_node(self, key_to_be_removed: int) -> None:
        if self.root:
            self.root = self.__remove_node(self.root, key_to_be_removed)

    def search_node(self, key: int) -> Node:
        if self.root:
            return self.__search_node(self.root, key)
        return None

    def print(self) -> None:
        if self.root is not None:
            if self.root.right is not None:
                self.__print(self.root.right, True, "")
            print(f"{self.root.key} (H={self.root.height})")
            if self.root.left is not None:
                self.__print(self.root.left, False, "")

    def reset(self) -> None:
        self.root = None

    def print_in_order(self) -> None:
        self.__print_in_order(self.root)

    def __insert_node(self, current_node: Node, node_to_be_inserted: Node) -> Node:
        if not current_node:
            return node_to_be_inserted

        if current_node.key > node_to_be_inserted.key:
            current_node.left = self.__insert_node(
                current_node.left, node_to_be_inserted
            )
        else:
            current_node.right = self.__insert_node(
                current_node.right, node_to_be_inserted
            )

        current_node.height = 1 + max(
            0 if not current_node.left else current_node.left.height,
            0 if not current_node.right else current_node.right.height,
        )

        return self.__handle_unbalanced_tree(current_node)

    def __remove_node(self, current_node: Node, key_to_be_removed: int) -> Node:
        if not current_node:
            return current_node

        if key_to_be_removed < current_node.key:
            current_node.left = self.__remove_node(current_node.left, key_to_be_removed)
        elif key_to_be_removed > current_node.key:
            current_node.right = self.__remove_node(
                current_node.right, key_to_be_removed
            )
        else:
            if current_node.left is None:
                temp_node = current_node.right
                current_node = None
                return temp_node

            elif current_node.right is None:
                temp_node = current_node.left
                current_node = None
                return temp_node

            temp_node = self.__get_highest_node(current_node.left)
            current_node.key = temp_node.key
            current_node.left = self.__remove_node(current_node.left, temp_node.key)

        if current_node is None:
            return current_node

        current_node.height = 1 + max(
            0 if current_node.left is None else current_node.left.height,
            0 if current_node.right is None else current_node.right.height,
        )

        return self.__handle_unbalanced_tree(current_node)

    def __search_node(self, current_node: Node, key: int) -> Node:
        if current_node:
            if current_node.key == key:
                return current_node
            elif current_node.key > key:
                return self.__search_node(current_node.left, key)
            else:
                return self.__search_node(current_node.right, key)
        return None

    def __get_highest_node(self, node: Node) -> Node:
        if node.right:
            return self.__get_highest_node(node.right)
        else:
            return node

    def __handle_unbalanced_tree(self, node: Node) -> Node:

        balance_factor = self.__calculate_balance_factor(node)
        right_child_balance_factor = self.__calculate_balance_factor(node.right)
        left_child_balance_factor = self.__calculate_balance_factor(node.left)

        if balance_factor > 1:
            if left_child_balance_factor < 0:
                print(
                    f"Chave {node.key} desbalanceada. Realizando Rotação Dupla à Direta"
                )
                return self.__perform_double_right_rotation(node)
            else:
                print(
                    f"Chave {node.key} desbalanceada. Realizando Rotação Simples à Direta"
                )
                return self.__perform_simple_right_rotation(node)

        if balance_factor < -1:
            if right_child_balance_factor > 0:
                print(
                    f"Chave {node.key} desbalanceada. Realizando Rotação Dupla à Esquerda"
                )
                return self.__perform_double_left_rotation(node)
            else:
                print(
                    f"Chave {node.key} desbalanceada. Realizando Rotação Simples à Esquerda"
                )
                return self.__perform_simple_left_rotation(node)

        return node

    def __calculate_balance_factor(self, node: Node) -> int:
        if not node:
            return 0

        left_children_height = 0 if not node.left else node.left.height
        right_children_height = 0 if not node.right else node.right.height

        return left_children_height - right_children_height

    def __perform_simple_right_rotation(self, node: Node) -> Node:
        temp_left = node.left
        temp_right = temp_left.right

        temp_left.right = node
        node.left = temp_right

        node.height = 1 + max(
            0 if not node.left else node.left.height,
            0 if not node.right else node.right.height,
        )

        temp_left.height = 1 + max(
            0 if not temp_left.left else temp_left.left.height,
            0 if not temp_left.right else temp_left.right.height,
        )

        return temp_left

    def __perform_simple_left_rotation(self, node: Node) -> Node:
        temp_right = node.right
        temp_left = temp_right.left

        temp_right.left = node
        node.right = temp_left

        node.height = 1 + max(
            0 if not node.left else node.left.height,
            0 if not node.right else node.right.height,
        )

        temp_right.height = 1 + max(
            0 if not temp_right.left else temp_right.left.height,
            0 if not temp_right.right else temp_right.right.height,
        )

        return temp_right

    def __perform_double_right_rotation(self, node: Node) -> Node:
        node.left = self.__perform_simple_left_rotation(node.left)
        return self.__perform_simple_right_rotation(node)

    def __perform_double_left_rotation(self, node: Node) -> Node:
        node.right = self.__perform_simple_right_rotation(node.right)
        return self.__perform_simple_left_rotation(node)

    def __print(self, current_node: Node, is_right_node: bool, indent: str) -> None:
        if current_node.right is not None:
            self.__print(
                current_node.right,
                True,
                indent + (" " * 12 if is_right_node else (" |" + " " * 10)),
            )
        print(indent, end="")
        if is_right_node:
            print(" /", end="")
        else:
            print(" \\", end="")

        print("---- ", end="")
        print(f"{current_node.key} (H={current_node.height})")
        if current_node.left is not None:
            self.__print(
                current_node.left,
                False,
                indent + (" " * 12 if not is_right_node else (" |" + " " * 10)),
            )

    def __print_in_order(self, current_node: Node) -> None:
        if current_node is None:
            return

        self.__print_in_order(current_node.left)
        print(f"{current_node.key} ", end="")
        self.__print_in_order(current_node.right)
