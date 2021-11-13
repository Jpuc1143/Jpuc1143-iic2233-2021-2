from PyQt5.QtCore import pyqtSignal, QObject

import parametros as p

class LogicStart(QObject):

    signal_user_submit_reply = pyqtSignal(bool)
    signal_start_game = pyqtSignal(str)

    def check_user(self, user):
        success = user.isalnum() and len(user) >= p.MIN_CARACTERES and len(user) <= p.MAX_CARACTERES
        self.signal_user_submit_reply.emit(success)

        if success:
            self.signal_start_game.emit(user)
