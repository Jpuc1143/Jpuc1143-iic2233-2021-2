from abc import ABC, abstractmethod
from threading import Thread, Condition
import json


class DCConnection(Thread, ABC):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.start()

        self.last_reply = None
        self.last_reply_condition = Condition()
    
    def run(self):
        while True:
            msg = self.recieve_msg()
            if msg["command"] == "reply":
                with self.last_reply_condition:
                    self.last_reply = msg["value"]
                    self.last_reply_condition.notify()
            else:
                reply = self.do_command(msg)
                if reply is not None:
                    self.send_command("reply", block=False, value=reply)

    def send_command(self, cmd, block=True, **kwargs):
        kwargs["command"] = cmd
        msg = json.dumps(kwargs)
        # TODO: encryptar
        self.sock.sendall(len(msg).to_bytes(4, byteorder="little"))
        self.sock.sendall(msg.encode("utf-8"))

        if not block:
            return

        with self.last_reply_condition as cv:
            self.last_reply_condition.wait_for(lambda: self.last_reply is not None)
            reply = self.last_reply
            self.last_reply = None

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
