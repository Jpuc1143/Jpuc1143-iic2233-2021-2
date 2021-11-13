from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class WindowPostGame(QWidget):
    signal_next_level = pyqtSignal()
    signal_save_score = pyqtSignal(str, int)
    signal_go_start = pyqtSignal()

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
        self.quit_button.clicked.connect(self.go_start)
        hbox.addWidget(self.quit_button)
        layout.addLayout(hbox, 5, 0, 1, 2)

    def show_results(self, victory, name, level, lives, score, coins):
        self.victory = victory
        self.name = name
        self.score = score
        if victory:
            self.next_level_button.setDisabled(False)
            self.message.setText(f"Nivel Completado {name}!")
        else:
            self.next_level_button.setDisabled(True)
            self.message.setText(f"Fin del Juego {name}")
            self.save_score(name, score)

        self.level_counter.setText(str(level))
        self.lives_counter.setText(str(lives))
        self.score_counter.setText(str(score))
        self.coin_counter.setText(str(coins))

        self.show()

    def next_level(self):
        self.hide()
        self.signal_next_level.emit()

    def save_score(self, name, score):
        self.signal_save_score.emit(name, score)

    def go_start(self):
        if self.victory:
            self.save_score(self.name, self.score)
        self.signal_go_start.emit()
        self.hide()
