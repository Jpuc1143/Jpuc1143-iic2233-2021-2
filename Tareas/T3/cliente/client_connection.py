from threading import Thread
from PyQt5.QtCore import pyqtSignal, QObject
from dcconnection import DCConnection
from endpoint_error import FatalEndpointError


class ClientConnection(DCConnection, QObject):
    signal_reply_received = pyqtSignal(object)
    signal_prompt_invite = pyqtSignal(str)
    signal_start_game = pyqtSignal(str, str, bool, int)
    signal_end_game = pyqtSignal(bool)

    def __init__(self, sock):
        DCConnection.__init__(self, sock)
        QObject.__init__(self)

    def send_command_signal(self, return_signal, cmd, **kwargs):
        def thread_func(caller, cmd, *args, **kwargs):
            caller.signal_reply_received.emit(caller.send_command(cmd, *args, **kwargs))

        try:
            self.signal_reply_received.disconnect()
        except TypeError:
            # Bloque intencionalmente dejado sin implementar.
            # https://stackoverflow.com/questions/21586643/pyqt-widget-connect-and-disconnect
            pass

        self.signal_reply_received.connect(return_signal)
        thread = Thread(
                target=thread_func, daemon=True,
                args=(self, cmd), kwargs=kwargs
                )
        thread.start()

    def do_command(self, msg):
        cmd = msg["command"]
        if cmd == "prompt_invite":
            inviter = msg["inviter"]
            self.signal_prompt_invite.emit(inviter)
            return

        elif cmd == "start_game":
            player = msg["player"]
            opponent = msg["opponent"]
            self.signal_start_game.emit(player, opponent, msg["starter"], msg["avatar"])
            return

        elif cmd == "end_game":
            self.signal_end_game.emit(msg["won"])
            self.send_command("logout", blocking=False)
            return

    def send_command(self, cmd, blocking=True, **kwargs):
        try:
            print("wrapped send")
            return super().send_command(cmd, blocking, **kwargs)
        except ConnectionError:
            raise FatalEndpointError

    def receive_msg(self):
        try:
            print("wrapped receive")
            return super().receive_msg()
        except ConnectionError:
            raise FatalEndpointError
