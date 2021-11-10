from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget

import parametros as p

class WindowRanking(QWidget):

    signal_return_start = pyqtSignal()
    signal_get_ranking = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DCCrossy Frog — Ranking")
        self.setGeometry(100, 100, 800, 600)  # TODO constantes

        # TODO: implementar mostrar ranking

        self.button_return = QPushButton("Volver", self)
        self.button_return.clicked.connect(self.return_start)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Aqui van los rankings", self))
        vbox.addWidget(self.button_return)

        self.setLayout(vbox)

    def return_start(self):
        self.hide()
        self.signal_return_start.emit()
