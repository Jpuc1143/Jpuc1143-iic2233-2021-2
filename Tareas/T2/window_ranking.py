from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout, QWidget

import parametros as p


class WindowRanking(QWidget):

    signal_return_start = pyqtSignal()
    signal_load_scores = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DCCrossy Frog — Ranking")
        self.move(p.WINDOW_OFFSET)

        self.button_return = QPushButton("Volver", self)
        self.button_return.clicked.connect(self.return_start)

        layout = QGridLayout()
        layout.addWidget(QLabel("Rankings", self), 0, 0, 1, 2)

        self.score_counter = []
        for index in range(1, 6):
            layout.addWidget(QLabel(str(index)), index, 0)
            self.score_counter.append(QLabel())
            layout.addWidget(self.score_counter[index-1], index, 1)

        layout.addWidget(self.button_return, 6, 0, 1, 2)

        self.setLayout(layout)

    def return_start(self):
        self.hide()
        self.signal_return_start.emit()

    def show_scores(self):
        self.signal_load_scores.emit()
        self.show()

    def set_scores(self, scores):
        for index, score in enumerate(scores):
            self.score_counter[index].setText(f"{score[1]} ({score[0]})")
        self.show()

    def closeEvent(self, event):
        self.return_start()
