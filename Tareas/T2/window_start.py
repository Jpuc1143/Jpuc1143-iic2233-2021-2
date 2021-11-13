from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap

import parametros as p


class WindowStart(QWidget):

    signal_submit_user = pyqtSignal(str)
    signal_show_ranking = pyqtSignal()

    def __init__(self):
        super().__init__()
 
        self.move(p.WINDOW_OFFSET)
        self.setWindowTitle("DCCrossy Frog")

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap(p.PATH_LOGO))
        self.logo.setScaledContents(True)

        self.user_entry = QLineEdit(self)

        self.button_play = QPushButton("Empezar", self)
        self.button_play.clicked.connect(self.submit_user)

        self.button_ranking = QPushButton("Ranking", self)
        self.button_ranking.clicked.connect(self.show_ranking)

        vbox = QVBoxLayout()
        vbox.addWidget(self.logo)
        vbox.addWidget(QLabel("Ingrese su nombre de usuario:", self))
        vbox.addWidget(self.user_entry)
        vbox.addWidget(self.button_play)
        vbox.addWidget(self.button_ranking)
        self.setLayout(vbox)

    def submit_user(self):
        self.signal_submit_user.emit(self.user_entry.text())

    def submit_user_reply(self, success):
        if success:
            self.hide()
        else:
            text = f"Usuario no valido. Tiene que ser alfanumérico y tener entre "\
                   f"{p.MIN_CARACTERES} y {p.MAX_CARACTERES} caracteres"
            self.user_entry.clear()
            self.user_entry.setPlaceholderText(text)

    def show_ranking(self):
        self.hide()
        self.signal_show_ranking.emit()
