from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QSpinBox, QPushButton, QRadioButton

from parameters import Parameters as p


class GameWindow(QWidget):
    signal_next_turn = pyqtSignal(int, int, bool)

    def __init__(self):
        super().__init__()
       
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

        self.next_turn_button = QPushButton(self)
        self.next_turn_button.clicked.connect(self.next_turn)

        layout = QGridLayout(self)
        layout.addWidget(self.player_marbles_label, 0, 0)
        layout.addWidget(self.bet_amount_input, 1, 0)
        layout.addWidget(self.bet_even_button, 0, 1)
        layout.addWidget(self.bet_odd_button, 1, 1)
        layout.addWidget(self.turn_label, 2, 0)
        layout.addWidget(self.next_turn_button, 2, 1)
        layout.addWidget(self.opponent_marbles_label, 3, 0)

    def start(self, player, opponent, starter):
        self.starter = starter
        self.turn = 0
        self.player_marbles = p.STARTING_MARBLES
        self.opponent_marbles = p.STARTING_MARBLES

        self.turn_label.setText(str(self.turn))
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
