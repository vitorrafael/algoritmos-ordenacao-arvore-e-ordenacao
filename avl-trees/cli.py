import avl_tree
import os

ACTIONS_WITH_ARGUMENTS = ["insert", "remove", "search"]
VALID_INPUT_ACTION_STRING = ["clear", "help", "exit", "print", "reset", "inorder",*ACTIONS_WITH_ARGUMENTS]

COMMANDS = """
Para modificar a AVL Tree ou extrair informações dela use os seguintes comandos:
\t- Inserir: insert <chave>
\t- Remover: remove <chave>
\t- Imprimir AVL Tree: print
\t- Buscar: search <chave>
\t- Imprimir em Order: inorder
\t- Resetar AVL Tree: reset
Outros comandos:
\t- Sair: exit
\t- Ajuda: help
\t- Limpar tela: clear
"""

WELCOME_MESSAGE = """Seja bem vindo a CLI da AVL Tree."""


class CLI:
    def __init__(self) -> None:
        self.avl_tree = avl_tree.AVLTree()
        self.actions = {
            "insert": self.insert_into_avl_tree,
            "remove": self.remove_from_avl_tree,
            "search": self.search_in_avl_tree,
            "print": self.print_avl_tree,
            "clear": self.clear_screen,
            "help": self.display_help,
            "exit": self.exit,
            "reset": self.reset_avl_tree,
            "inorder": self.print_avl_tree_in_order
        }
        self.execute = True

    def start(self) -> None:
        print(WELCOME_MESSAGE + COMMANDS)

        while self.execute:
            user_input = self.request_user_input()

            if not self.is_user_input_valid(user_input):
                print("Comando inválido!\nVerifique o comando e os argumentos passados")
            else:
                input_action = self.parse_user_input(user_input)
                self.actions[input_action[0]](input_action[1])

            print("")

    def request_user_input(self) -> str:
        user_input = input("> ").strip()
        return user_input

    def is_user_input_valid(self, input: str) -> bool:
        input_arguments = input.split(" ")
        action = input_arguments[0].lower()

        if action in VALID_INPUT_ACTION_STRING:
            return (
                action in ACTIONS_WITH_ARGUMENTS
                and len(input_arguments) == 2
                and self.__is_numeric(input_arguments[1])
            ) or (action not in ACTIONS_WITH_ARGUMENTS and len(input_arguments) == 1)
        else:
            return False

    def __is_numeric(self, string: str) -> bool:
        return string.strip("-").isnumeric()

    def parse_user_input(self, input: str) -> tuple:
        input_parts = input.split(" ")
        action = input_parts[0].lower()
        argument = None if len(input_parts) == 1 else input_parts[1]
        return tuple([action, argument])

    def insert_into_avl_tree(self, key: int) -> None:
        self.avl_tree.insert_node(int(key))
        self.avl_tree.print()

    def remove_from_avl_tree(self, key: int) -> None:
        self.avl_tree.remove_node(int(key))
        self.avl_tree.print()

    def print_avl_tree(self, key: None) -> None:
        self.avl_tree.print()

    def search_in_avl_tree(self, key: int) -> None:
        node = self.avl_tree.search_node(int(key))
        if not node:
            print("Chave não encontrada na AVL Tree")
        else:
            print(f"Chave encontrada: {node}")

    def clear_screen(self, *args) -> None:
        if os.name == "posix": # Linux or Mac
            os.system("clear")
        else: # Windows
            os.system("cls")

    def exit(self, *args) -> None:
        self.execute = False

    def display_help(self, *args) -> None:
        print(COMMANDS)

    def reset_avl_tree(self, *args) -> None:
        self.avl_tree.reset()
        self.avl_tree.print()

    def print_avl_tree_in_order(self, *args) -> None:
        self.avl_tree.print_in_order()
