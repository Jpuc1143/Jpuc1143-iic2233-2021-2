from threading import Thread
from PyQt5.QtCore import pyqtSignal, QObject
from dcconnection import DCConnection


class ClientConnection(DCConnection, QObject):
    signal_reply_received = pyqtSignal(object)
    signal_prompt_invite = pyqtSignal(str)

    def __init__(self, sock):
        DCConnection.__init__(self, sock)
        QObject.__init__(self)

    def send_command_signal(self, return_signal, cmd, **kwargs):
        def thread_func(caller, cmd, *args, **kwargs):
            caller.signal_reply_received.emit(caller.send_command(cmd, *args, **kwargs))

        self.signal_reply_received.connect(return_signal)
        thread = Thread(
                target=thread_func,
                args=(self, cmd), kwargs=kwargs
                )
        thread.start()

    def do_command(self, msg):
        cmd = msg["command"]
        if cmd == "prompt_invite":
            inviter = msg["inviter"]
            self.signal_prompt_invite.emit(inviter)
            return
