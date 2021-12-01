import sys
from socket import socket

from PyQt5.QtWidgets import QApplication

from client import Client

from start_window import StartWindow
from start_logic import StartLogic
from main_window import MainWindow

# Código de contenidos Semana 7.1
# https://github.com/IIC2233/contenidos/blob/main/semana-07/1-interfaces-gr%C3%A1ficas.ipynb
if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    
    # TODO hacer esto correctamente y eliminar prueba
    sock = socket()
    sock.connect(("localhost", 8080))
    client = Client(sock)
    #client.send_command("ping", reply=False)
    #print(client.send_command("echo", value="test"))

    app = QApplication([])
    
    start_window = StartWindow()
    start_logic = StartLogic(client)

    main_window = MainWindow()

    start_window.signal_verify_user.connect(
            start_logic.verify_user
            )

    start_logic.signal_verify_user_reply.connect(
            start_window.verify_user_reply
            )

    start_logic.signal_login.connect(
            main_window.show
            )
    
    start_window.show()
    app.exec()
