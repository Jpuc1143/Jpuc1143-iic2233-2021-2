from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QSpinBox, QPushButton, QRadioButton, QGroupBox
from PyQt5.QtGui import QPixmap

from parameters import Parameters as p


class GameWindow(QWidget):
    signal_next_turn = pyqtSignal(int, int, bool)
    signal_end_game = pyqtSignal(bool, str, str)

    def __init__(self):
        super().__init__()
       
        self.player_label = QLabel()
        self.player_avatar = QLabel()
        self.player_avatar.setMaximumSize(p.SIZE_AVATAR)
        self.player_avatar.setScaledContents(True)

        self.opponent_label = QLabel()
        self.opponent_avatar = QLabel()
        self.opponent_avatar.setMaximumSize(p.SIZE_AVATAR)
        self.opponent_avatar.setScaledContents(True)

        self.player_marbles = p.STARTING_MARBLES
        self.player_marbles_label = QLabel(str(self.player_marbles))
        self.opponent_marbles = p.STARTING_MARBLES
        self.opponent_marbles_label = QLabel(str(self.opponent_marbles))

        self.bet_amount_input = QSpinBox()
        self.bet_amount_input.setSuffix(" canicas")
        self.bet_amount_input.setMinimum(1)
        self.bet_amount_input.setMaximum(self.player_marbles)

        self.bet_even_button = QRadioButton("Par")
        self.bet_odd_button = QRadioButton("Impar")

        self.turn = 0
        self.turn_label = QLabel(str(self.turn))

        self.next_turn_button = QPushButton("Fin Turno", self)
        self.next_turn_button.clicked.connect(self.next_turn)

        layout = QGridLayout(self)
        layout.addWidget(self.player_avatar, 0, 0)
        layout.addWidget(self.player_label, 1, 0)
        layout.addWidget(self.player_marbles_label, 0, 1)
        layout.addWidget(self.bet_amount_input, 1, 1)
        layout.addWidget(self.bet_even_button, 0, 2)
        layout.addWidget(self.bet_odd_button, 1, 2)

        layout.addWidget(self.turn_label, 2, 0)
        layout.addWidget(self.next_turn_button, 2, 1, 1, 2)

        layout.addWidget(self.opponent_avatar, 3, 2)
        layout.addWidget(self.opponent_label, 4, 2)
        layout.addWidget(self.opponent_marbles_label, 3, 0)

    def start(self, player, opponent, starter, avatar):
        self.player = player
        self.player_label.setText(player + " (Tú)")
        self.player_label.repaint()
        self.opponent = opponent
        self.opponent_label.setText(opponent)
        self.opponent_label.repaint()

        if avatar == 0:
            self.player_avatar.setPixmap(QPixmap(p.PATH_AVATAR_0))
            self.opponent_avatar.setPixmap(QPixmap(p.PATH_AVATAR_1))
        else:
            self.player_avatar.setPixmap(QPixmap(p.PATH_AVATAR_1))
            self.opponent_avatar.setPixmap(QPixmap(p.PATH_AVATAR_0))

        self.starter = starter
        self.turn = 0
        self.player_marbles = p.STARTING_MARBLES
        self.opponent_marbles = p.STARTING_MARBLES

        self.turn_label.setText("Turno: " + str(self.turn))
        self.turn_label.repaint()

        self.player_marbles_label.setText(str(self.player_marbles))
        self.player_marbles_label.repaint()

        self.opponent_marbles_label.setText(str(self.opponent_marbles))
        self.opponent_marbles_label.repaint()

        self.bet_amount_input.setValue(1)
        self.bet_amount_input.setMaximum(self.player_marbles)
 
        self.bet_even_button.setChecked(True)
        self.bet_even_button.setEnabled(self.starter)
        self.bet_odd_button.setEnabled(self.starter)

        self.show()

    def next_turn(self):
        self.next_turn_button.setEnabled(False)
        self.bet_amount_input.setEnabled(False)
        self.bet_even_button.setEnabled(False)
        self.bet_odd_button.setEnabled(False)

        self.signal_next_turn.emit(
                self.turn, self.bet_amount_input.value(),
                self.bet_odd_button.isChecked()
                )

    def display_next_turn(self, won_round, player_marbles, opponent_marbles):
        self.turn += 1
        self.turn_label.setText(str(self.turn))
        self.turn_label.repaint()

        self.player_marbles = player_marbles
        self.player_marbles_label.setText(str(self.player_marbles))
        self.player_marbles_label.repaint()

        self.opponent_marbles = opponent_marbles
        self.opponent_marbles_label.setText(str(self.opponent_marbles))
        self.opponent_marbles_label.repaint()

        self.bet_amount_input.setValue(1)
        self.bet_amount_input.setMaximum(self.player_marbles)

        self.next_turn_button.setEnabled(True)
        self.bet_amount_input.setEnabled(True)

        if (self.turn % 2 == 0) == self.starter:
            self.bet_even_button.setEnabled(True)
            self.bet_odd_button.setEnabled(True)

    def end_game(self, won):
        self.close()
        self.signal_end_game.emit(won, self.player, self.opponent)
