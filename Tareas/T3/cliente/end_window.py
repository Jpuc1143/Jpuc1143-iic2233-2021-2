from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap

from parameters import Parameters as p


class EndWindow(QWidget):
    signal_go_back = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fin")

    def end_game(self, won, player, opponent):
        layout = QGridLayout(self)
        layout.addWidget(QLabel("Victoria!" if won else "Derrota..."), 0, 0)
        layout.addWidget(QLabel(player), 1, 0)

        label = QLabel()
        label.setScaledContents(True)
        label.setPixmap(QPixmap(p.PATH_MONEY if won else p.PATH_DEAD))
        layout.addWidget(label, 1, 1)
        label.setMaximumSize(p.SIZE_ICON)

        layout.addWidget(QLabel(opponent), 2, 0)
        label = QLabel()
        label.setScaledContents(True)
        label.setPixmap(QPixmap(p.PATH_MONEY if not won else p.PATH_DEAD))
        label.setMaximumSize(p.SIZE_ICON)
        layout.addWidget(label, 2, 1)

        button = QPushButton("Volver")
        button.clicked.connect(self.go_back)
        layout.addWidget(button, 3, 0)

        self.show()

    def go_back(self):
        self.signal_go_back.emit()
        self.close()
