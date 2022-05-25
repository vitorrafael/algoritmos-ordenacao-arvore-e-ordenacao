from typing import Any
from node import Node


class AVLTree:
    def __init__(self) -> None:
        self.root: Node = None
    
    def insert_node(self, node_key: Any) -> Node:
        node_to_be_inserted = Node(node_key)
        if not self.root:
            self.root = node_to_be_inserted
        else:
            self.__insert_node(self.root, node_to_be_inserted)

    def remove_node(self, key_to_be_removed: int) -> None:
        if self.root:
            self.__remove_node(self.root, key_to_be_removed)

    def __insert_node(self, current_node: Node, node_to_be_inserted: Node) -> Node:
        if not current_node:
            return node_to_be_inserted
        
        if current_node.key < node_to_be_inserted.key:
            current_node.left = self.__insert_node(current_node.left, node_to_be_inserted)
        else:
            current_node.right = self.__insert_node(current_node.right, node_to_be_inserted)

        current_node.height = 1 + max(
            -1 if not current_node.left else current_node.left.height, 
            -1 if not current_node.right else current_node.right
        )

        return self.__handle_unbalanced_tree(current_node)

    def __remove_node(self, current_node: Node, key_to_be_removed: int) -> Node:
        if not current_node:
            return current_node
        
        if key_to_be_removed < current_node.key:
            current_node.left = self.__remove_node(current_node.left, key_to_be_removed)
        elif key_to_be_removed > current_node.key:
            current_node.right = self.__remove_node(current_node.right, key_to_be_removed)
        else:
            if not current_node.left and not current_node.right:
                del current_node
                return None
            
            if not current_node.left:
                temp_node = current_node.right
                del current_node
                return temp_node
            elif not current_node.right:
                temp_node = current_node.left
                del current_node
                return temp_node

            temp_node = self.__get_highest_node(current_node.left)
            current_node.key = temp_node.key
            current_node.left = self.__remove_node(current_node.left, temp_node.key)

        if not current_node:
            return current_node

        height = 1 + max(
            -1 if not current_node.left else current_node.left.height, 
            -1 if not current_node.right else current_node.right
        )

        current_node.height = height

        return self.__handle_unbalanced_tree(current_node)

    def __get_highest_node(self, node: Node) -> Node:
        if node.right:
            return self.__get_highest_node(node.right)
        else:
            return node

    def __handle_unbalanced_tree(self, node: Node) -> Node:

        balance_factor = self.__calculate_balance_factor(node)
        right_child_balance_factor = self.__calculate_balance_factor(node.right)
        left_child_balance_factor = self.__calculate_balance_factor(node.left)

        # Rotação Simples à Direita
        if balance_factor > 1 and left_child_balance_factor > 0:
            return self.__perform_simple_right_rotation(node)

        # Rotação Simples à Esquerda
        if balance_factor < -1 and right_child_balance_factor < 0:
            return self.__perform_simple_left_rotation(node)

        # Rotação Dupla à Direita
        if balance_factor > 1 and left_child_balance_factor < 0:
            return self.__perform_double_right_rotation(node)

        # Rotação Dupla à Esquerda
        if balance_factor < -1 and right_child_balance_factor > 0:
            return self.__perform_double_left_rotation(node)

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

        height = 1 + max(
            -1 if not node.left else node.left.height, 
            -1 if not node.right else node.right
        )

        node.height = height
        temp_left.height = height

        return temp_left

    def __perform_simple_left_rotation(self, node: Node) -> Node:
        temp_right = node.right
        temp_left = temp_right.left

        temp_right.left = node
        node.right = temp_left

        height = 1 + max(
            -1 if not node.left else node.left.height, 
            -1 if not node.right else node.right
        )

        node.height = height
        temp_left.height = height

        return temp_right

    def __perform_double_right_rotation(self, node: Node) -> Node:
        node.left = self.__perform_simple_left_rotation(node.left)
        return self.__perform_simple_right_rotation(node)

    def __perform_double_left_rotation(self, node: Node) -> Node:
        node.right = self.__perform_simple_right_rotation(node.right)
        return self.__perform_simple_left_rotation(node)
