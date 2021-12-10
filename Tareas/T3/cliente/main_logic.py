from PyQt5.QtCore import pyqtSignal, QObject, QTimer


class MainLogic(QObject):
    signal_update_lobby = pyqtSignal(list)
    signal_invite_player_reply = pyqtSignal(bool)

    def __init__(self, client):
        super().__init__()
        
        self.client = client

        self.timer_update_lobby = QTimer()
        self.timer_update_lobby.setInterval(2000) #TODO parametro
        self.timer_update_lobby.timeout.connect(self.update_lobby)

    def join_lobby(self):
        self.timer_update_lobby.start()
        self.update_lobby()

    def exit_lobby(self):
        self.timer_update_lobby.stop()

    def update_lobby(self):
        lobby_data = self.client.send_command("query-lobby")
        self.signal_update_lobby.emit(lobby_data)

    def invite_player(self, invited_user):
        self.client.send_command_signal(self.invite_player_finished, "invite", invited=invited_user)

    def invite_player_finished(self, success):
        print(self.sender())
        print("estado de invitacion", success)
        self.signal_invite_player_reply.emit(success)

    def prompt_invite_reply(self, accepted):
        self.client.send_command("reply", blocking=False, value=accepted, replied_command="prompt_invite")

