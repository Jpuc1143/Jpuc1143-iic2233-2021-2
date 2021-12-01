from abc import ABC, abstractmethod
from threading import Thread
import json
# test

class DCCalamar(Thread, ABC):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.start()

        self.last_reply = None
    
    def run(self):
        while True:
            msg = self.recieve_msg()
            if msg["command"] == "reply":
                self.last_reply = msg["value"]
            else:
                reply = self.do_command(msg)
                if reply is not None:
                    print("sending reply", reply)
                    self.send_command("reply", value=reply)

    def send_command(self, cmd, reply=True, **kwargs):
        kwargs["command"] = cmd
        print(f"sending {kwargs}")
        msg = json.dumps(kwargs)
        # TODO: encryptar
        self.sock.sendall(len(msg).to_bytes(4, byteorder="little"))
        self.sock.sendall(msg.encode("utf-8"))

        # TODO hacer esto correctamente
        if not reply:
            return
        while self.last_reply is None:
            pass
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
            print(f"buffer {buf} msg {msg}")
        return json.loads(msg)

    @abstractmethod
    def do_command(self, cmd, **kwargs):
        pass
