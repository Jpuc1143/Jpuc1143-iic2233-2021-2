from PyQt5.QtCore import pyqtSignal, QObject

from abc import abstractmethod
from threading import Thread, Condition
import json

from parameters import Parameters as p

class DCConnection(Thread):
    def __init__(self, sock):
        super().__init__(daemon=True)
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
                thread = Thread(target=self.process_reply, args=(msg,), daemon=True)
                thread.start()

    def process_reply(self, msg):
        reply = self.do_command(msg)
        if reply is not None:
            self.send_command("reply", blocking=False, value=reply, replied_command=msg["command"])

    def send_command(self, cmd, blocking=True, **kwargs):
        # TODO el padding esta siendo eliminado al enviar mensaje. Revizar más tarde
        kwargs["command"] = cmd
        plaintext = json.dumps(kwargs)
        #plaintext =  "a" + "b" * 78 + "c" + "e" + "\0"
        print("enviando", plaintext)

        cyphertext = self.encrypt_msg(plaintext)

        self.sock.sendall(len(cyphertext).to_bytes(4, byteorder="little"))
        
        blocks_num = (len(cyphertext)//p.BLOCK_SIZE)+(0 if len(cyphertext)%p.BLOCK_SIZE==0 else 1)
        print("blocks num", blocks_num)
        for block_index in range(blocks_num):
            block = cyphertext[
                    block_index*p.BLOCK_SIZE:
                    min(block_index+p.BLOCK_SIZE, len(cyphertext))
                    ]
            #block = "" if block is None else block
            block = block.encode("utf-8")
            print("enviando bloque", block)
            self.sock.sendall(block_index.to_bytes(4, byteorder="big"))
            self.sock.sendall(block)
            #.ljust(p.BLOCK_SIZE, b"\x00")
        
        if not blocking:
            return

        with self.last_reply_condition:
            self.last_reply_condition.wait_for(lambda: cmd in self.last_reply)
            reply = self.last_reply[cmd]
            del self.last_reply[cmd]

        return reply

    def encrypt_msg(self, plaintext):
        return plaintext

    def recieve_msg(self):
        buf = self.sock.recv(4)
        print("len recivido", buf)
        if buf == b"":
            print("error conexcion")
            raise ConnectionError
        cyphertext_size = int.from_bytes(buf, byteorder="little")
        print("len size", cyphertext_size)
        blocks_num = (cyphertext_size//p.BLOCK_SIZE)+(0 if cyphertext_size%p.BLOCK_SIZE==0 else 1)
        print("blocks num", blocks_num)

        msg_size = cyphertext_size + 4*blocks_num
        print("expected msgsize", msg_size)

        msg = bytearray()
        while msg_size > len(msg):
            buf = self.sock.recv(min(4096, msg_size-len(msg)))
            msg += buf
        if msg == b"":
            raise ConnectionError

        print("structured", msg)
        cyphertext = bytearray()
        print(blocks_num)
        for block_index in range(blocks_num):
            block = msg[block_index*(p.BLOCK_SIZE+4)+4:block_index*(p.BLOCK_SIZE+4)+4+p.BLOCK_SIZE]
            print(block)
            cyphertext += block

        plaintext = self.decrypt_msg(cyphertext)

        print("msg", plaintext)
        return json.loads(plaintext)

    def decrypt_msg(self, cyphertext):
        return cyphertext

    @abstractmethod
    def do_command(self, cmd, **kwargs):
        pass
