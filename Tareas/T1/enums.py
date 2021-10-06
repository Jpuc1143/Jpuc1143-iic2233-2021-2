from enum import Enum, auto


class Menu(Enum):
    START = auto()
    MAIN = auto()
    EXIT = auto()
    CHOOSE_TRIBUTE = auto()
    SHOW_CANDIDATE_TRIBUTE = auto()
    CONFIRM_TRIBUTE = auto()
    CHOOSE_ARENA = auto()
    NEW_ARENA = auto()
    LOAD_MENU = auto()
    LOAD = auto()
    DELETE_MENU = auto()
    DELETE = auto()

    ACTIONS = auto()
    HEROIC = auto()
    CHOOSE_TARGET = auto()
    ATTACK = auto()
    BEG = auto()
    BALL_MODE = auto()
    FORFEIT = auto()

    STATUS = auto()
    SIMULATE = auto()
    INVENTORY = auto()
    USE_ITEM = auto()
    SUMMARY = auto()
