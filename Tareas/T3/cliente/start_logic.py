from PyQt5.QtCore import QObject, pyqtSignal


class StartLogic(QObject):
    signal_verify_user_reply = pyqtSignal(bool)
    signal_login = pyqtSignal(str)

    def __init__(self, client):
        super().__init__()
        self.client = client

    def verify_user(self, user, birthday):
        success = self.client.send_command("login", user=user, birthday=birthday)
        self.signal_verify_user_reply.emit(success)
        
        if success:
            self.signal_login.emit(user)
