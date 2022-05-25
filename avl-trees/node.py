from typing import Any


class Node:
    def __init__(self, key: int) -> None:
        self.key = key
        self.left: Node = None
        self.right: Node = None
        self.height: int = 0

    def has_both_children(self) -> bool:
        return self.has_left_child() and self.has_right_child()

    def has_left_child(self) -> bool:
        return bool(self.left)

    def has_right_child(self) -> bool:
        return bool(self.right)