from PyQt5.QtCore import pyqtSignal, QObject, QTimer


class MainLogic(QObject):
    signal_update_lobby = pyqtSignal(list)

    def __init__(self, client):
        super().__init__()
        
        self.client = client

        self.timer_update_lobby = QTimer()
        self.timer_update_lobby.setInterval(500) #TODO parametro
        self.timer_update_lobby.timeout.connect(self.update_lobby)

    def join_lobby(self):
        self.timer_update_lobby.start()

    def exit_lobby(self):
        self.timer_update_lobby.stop()

    def update_lobby(self):
        lobby_data = self.client.send_command("query-lobby")
        self.signal_update_lobby.emit(lobby_data)
