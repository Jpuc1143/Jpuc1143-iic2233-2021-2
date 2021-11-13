from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class WindowPostGame(QWidget):
    signal_next_level = pyqtSignal()

    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("DCCrossy Frog — Resultados")

        self.message = QLabel("TITLE")
        self.level_counter = QLabel("num")
        self.lives_counter = QLabel("num")
        self.score_counter = QLabel("num")
        self.coin_counter = QLabel("num")

        layout = QGridLayout(self)
        layout.addWidget(self.message, 0, 0, 1, 2)
        layout.addWidget(QLabel("Nivel:  "), 1, 0)
        layout.addWidget(self.level_counter, 1, 1)
        layout.addWidget(QLabel("Vidas:  "), 3, 0)
        layout.addWidget(self.lives_counter, 3, 1)
        layout.addWidget(QLabel("Score:  "), 2, 0)
        layout.addWidget(self.score_counter, 2, 1)
        layout.addWidget(QLabel("Monedas:"), 4, 0)
        layout.addWidget(self.coin_counter, 4, 1)
        
        hbox = QHBoxLayout()
        self.next_level_button = QPushButton("Siguiente")
        self.next_level_button.clicked.connect(self.next_level)
        hbox.addWidget(self.next_level_button)
        self.quit_button = QPushButton("Salir")
        hbox.addWidget(self.quit_button)
        layout.addLayout(hbox, 5, 0, 1, 2)

    def show_results(self, victory, level, lives, score, coins):
        if victory:
            self.next_level_button.setDisabled(False)
            self.message.setText("Nivel Completado!")
        else:
            self.next_level_button.setDisabled(True)
            self.message.setText("Fin del Juego")

        self.level_counter.setText(str(level))
        self.lives_counter.setText(str(lives))
        self.score_counter.setText(str(score))
        self.coin_counter.setText(str(coins))

        self.show()

    def next_level(self):
        self.hide()
        self.signal_next_level.emit()
