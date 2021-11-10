from PyQt5.QtCore import pyqtSignal, QObject


class LogicStart(QObject):

    self.signal_user_submit_reply = pyqtSignal(bool)
    self.signal_start_game = pyqtSignal(str)

    def check_user(user):
        success = user.isalpha() && len(user) >= p.MIN_CARACTERES && len(user) <= p.MAX_CARACTERES
        
        self.signal_user_submit_reply.emit(success)

        if success:
            self.signal_start_game.emit(user)
