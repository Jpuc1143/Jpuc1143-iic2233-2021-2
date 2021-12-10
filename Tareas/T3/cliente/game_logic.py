from PyQt5.QtCore import pyqtSignal, QObject


class GameLogic(QObject):
    signal_display_next_turn = pyqtSignal(bool, int, int)

    def __init__(self, client):
        super().__init__()

        self.client = client

    def next_turn(self, current_turn, bet_amount, bet_is_odd):
        self.client.send_command_signal(
                self.display_next_turn, "next_turn",
                turn=current_turn, bet_amount=bet_amount, bet_is_odd=bet_is_odd
                )

    def display_next_turn(self, turn_results):
        print("results", turn_results)
        self.signal_display_next_turn.emit(*turn_results)
