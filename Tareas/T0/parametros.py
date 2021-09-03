from enum import Enum, auto

# Mínimo de caracteres que debe tener el nombre de un nuevo usuario
MIN_CARACTERES = 1

# Máximo de caracteres que debe tener le nombre de un nuevo usuario
MAX_CARACTERES = 15


# TODO: Citar codigo de enum https://docs.python.org/3/library/enum.html?highlight=enum
class Menu(Enum):
    START = auto()
    MAIN = auto()
    POSTS = auto()
    VIEW_POST = auto()
    EXIT = auto()
    LOGIN = auto()
    PUBLISH_COMMENT = auto()
    REGISTER = auto()
    SELF_POSTS = auto()
    PUBLISH_POST = auto()
    DELETE_POST = auto()
