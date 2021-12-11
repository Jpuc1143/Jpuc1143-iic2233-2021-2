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
        kwargs["command"] = cmd
        plaintext = json.dumps(kwargs)
        print("enviando", plaintext)
        
        cyphertext = bytearray(self.encrypt_msg(plaintext.encode("utf-8")))
        self.sock.sendall(len(cyphertext).to_bytes(4, byteorder="little"))

        blocks_num = (len(cyphertext)//p.BLOCK_SIZE)+(0 if len(cyphertext)%p.BLOCK_SIZE==0 else 1)
        for block_index in range(blocks_num):
            block = bytearray(cyphertext[
                    block_index*p.BLOCK_SIZE:
                    min(block_index*p.BLOCK_SIZE+p.BLOCK_SIZE, len(cyphertext))
                    ])
            if len(block) < p.BLOCK_SIZE:
                block.extend(bytearray(p.BLOCK_SIZE - len(block)))
            self.sock.sendall(block_index.to_bytes(4, byteorder="big"))
            self.sock.sendall(block)
        
        if not blocking:
            return

        with self.last_reply_condition:
            self.last_reply_condition.wait_for(lambda: cmd in self.last_reply)
            reply = self.last_reply[cmd]
            del self.last_reply[cmd]

        return reply

    def encrypt_msg(self, plaintext):
        # Encriptación sin llaves; 100% efectiva.
        A = bytearray()
        B = bytearray()
        C = bytearray()
        for index, byte in enumerate(plaintext):
            if index % 3 == 0:
                A.append(byte)
            elif index % 3 == 1:
                B.append(byte)
            elif index % 3 == 2:
                C.append(byte)
        
        if B[0] > C[0]:
            result = bytearray(A + B + C)
            print("preswap", result)
            for index, byte in enumerate(result):
                print("byte", byte)
                if result[index:index+1] == b"\x05":
                    print("5 to 3")
                    result[index:index+1] = b"\x03"
                elif result[index:index+1] == b"\x03":
                    print("3 to 5")
                    result[index:index+1] = b"\x05"
            result += b"\x00"
        else:
            result = bytearray(B + A + C)
            result += b"\x01"

        print("cyphertext", result)
        return result

    def recieve_msg(self):
        buf = self.sock.recv(4)
        print("len recivido", buf)
        if buf == b"":
            print("error conexcion")
            raise ConnectionError
        cyphertext_size = int.from_bytes(buf, byteorder="little")
        blocks_num = (cyphertext_size//p.BLOCK_SIZE)+(0 if cyphertext_size%p.BLOCK_SIZE==0 else 1)

        msg_size = p.BLOCK_SIZE * blocks_num + 4*blocks_num

        msg = bytearray()
        while msg_size > len(msg):
            buf = self.sock.recv(min(4096, msg_size-len(msg)))
            msg += buf
        if msg == b"":
            raise ConnectionError

        cyphertext = bytearray()
        for block_index in range(blocks_num):
            block = msg[block_index*(p.BLOCK_SIZE+4)+4:block_index*(p.BLOCK_SIZE+4)+4+p.BLOCK_SIZE]
            cyphertext += block
        
        plaintext = self.decrypt_msg(cyphertext[:cyphertext_size])
        
        print("msg", plaintext)
        return json.loads(plaintext)

    def decrypt_msg(self, cyphertext):
        min_size = len(cyphertext[:-1]) // 3
        remainder_size = len(cyphertext[:-1]) % 3

        cyphertext_copy = cyphertext.copy()
        if cyphertext[-1:] == b"\x00":
            for index, byte in enumerate(cyphertext[:-1]):
                if cyphertext[index:index+1] == b"\x05":
                    cyphertext[index:index+1] = b"\x03"
                elif cyphertext[index:index+1] == b"\x03":
                    cyphertext[index:index+1] = b"\x05"
    
            A = cyphertext[:min_size + (1 if remainder_size >= 1 else 0)]
            del cyphertext[:min_size + (1 if remainder_size >= 1 else 0)]
            B = cyphertext[:min_size + (1 if remainder_size >= 2 else 0)]
            del cyphertext[:min_size + (1 if remainder_size >= 2 else 0)]
            C = cyphertext[:-1]
        
        else:
            B = cyphertext[:min_size + (1 if remainder_size >= 2 else 0)]
            del cyphertext[:min_size + (1 if remainder_size >= 2 else 0)]
            A = cyphertext[:min_size + (1 if remainder_size >= 1 else 0)]
            del cyphertext[:min_size + (1 if remainder_size >= 1 else 0)]
            C = cyphertext[:-1]

        result = bytearray()
        print(A, B, C)
        for index in range(len(cyphertext_copy[:-1])):
            print("index", index, cyphertext_copy[index])
            if index % 3 == 0:
                result.append(A[index//3])
            elif index % 3 == 1:
                result.append(B[index//3])
            elif index % 3 == 2:
                result.append(C[index//3])

        print("result", result)
        return result

    @abstractmethod
    def do_command(self, cmd, **kwargs):
        pass
