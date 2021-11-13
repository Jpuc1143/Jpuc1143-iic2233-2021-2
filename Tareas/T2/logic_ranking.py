from PyQt5.QtCore import QObject, pyqtSignal

import parametros as p


class LogicRanking(QObject):
    signal_set_scores = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()

    def load_scores(self):
        scores = []
        try:
            with open(p.PATH_SCORES, "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip("\n").split(",", maxsplit=1)
                    data[0] = int(data[0])
                    scores.append(data)
        except FileNotFoundError:
            print(f"Archivo {p.PATH_SCORES} no existe")

        self.signal_set_scores.emit(sorted(scores, reverse=True)[0:5])
