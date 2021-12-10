from PyQt5.QtCore import pyqtSignal, QObject

from abc import abstractmethod
from threading import Thread, Condition
import json


class DCConnection(Thread):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.start()

        self.last_reply = dict()
        self.last_reply_condition = Condition()
    
    def run(self):
        while True:
            msg = self.recieve_msg()
            print("received", msg)
            if msg["command"] == "reply":
                with self.last_reply_condition:
                    self.last_reply[msg["replied_command"]] = msg["value"]
                    self.last_reply_condition.notify_all()
            else:
                thread = Thread(target=self.process_reply, args=(msg,))
                thread.start()

    def process_reply(self, msg):
        reply = self.do_command(msg)
        if reply is not None:
            self.send_command("reply", blocking=False, value=reply, replied_command=msg["command"])

    def send_command(self, cmd, blocking=True, **kwargs):
        kwargs["command"] = cmd
        msg = json.dumps(kwargs)
        print("enviando", msg)
        # TODO: encryptar
        self.sock.sendall(len(msg).to_bytes(4, byteorder="little"))
        self.sock.sendall(msg.encode("utf-8"))

        if not blocking:
            return

        with self.last_reply_condition:
            self.last_reply_condition.wait_for(lambda: cmd in self.last_reply)
            reply = self.last_reply[cmd]
            del self.last_reply[cmd]

        return reply

    def recieve_msg(self):
        msg_size = int.from_bytes(self.sock.recv(4), byteorder="little")
        # TODO desencriptar y ajustar tamaño
        msg = bytearray()
        while msg_size > len(msg):
            buf = self.sock.recv(min(4096, msg_size-len(msg)))
            msg += buf
        return json.loads(msg)

    @abstractmethod
    def do_command(self, cmd, **kwargs):
        pass
