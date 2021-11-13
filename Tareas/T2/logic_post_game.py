from PyQt5.QtCore import QObject
import parametros as p


class LogicPostGame(QObject):
    def __init__(self):
        super().__init__()

    def save_score(self, name, score):
        with open(p.PATH_SCORES, "a", encoding="utf-8") as file:
            file.write(f"{score},{name}\n")
