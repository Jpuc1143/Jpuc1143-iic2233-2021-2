import sys
from PyQt5.QtWidgets import QApplication

from window_game import WindowGame
from window_start import WindowStart


# Codigo copiado de contenidos Semana 7.1
# https://github.com/IIC2233/contenidos/blob/main/semana-07/1-interfaces-gr%C3%A1ficas.ipynb
if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])

    window_start = WindowStart()
    window_game = WindowGame()

    app.exec()
