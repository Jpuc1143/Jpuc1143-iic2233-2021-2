import sys
import threading
from socket import socket

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from client_connection import ClientConnection
from endpoint_error import EndpointError, FatalEndpointError
from parameters import Parameters as p

from start_window import StartWindow
from start_logic import StartLogic
from main_window import MainWindow
from main_logic import MainLogic
from game_window import GameWindow
from game_logic import GameLogic

# Código de contenidos Semana 7.1
# https://github.com/IIC2233/contenidos/blob/main/semana-07/1-interfaces-gr%C3%A1ficas.ipynb
if __name__ == '__main__':
    def hook(type, value, traceback):
        if isinstance(value, EndpointError):
            value.show_error()
            if type == FatalEndpointError:
                QApplication.exit(1)
        elif isinstance(value, ConnectionError):
            FatalEndpointError().show_error()
            QApplication.exit(1)
        else:
            sys.__excepthook__(type, value, traceback)
    
    def thread_hook(args):
        print(args)
        hook(args.exc_type, args.exc_value, args.exc_traceback)

    sys.excepthook = hook
    threading.excepthook = thread_hook
    
    # TODO hacer esto correctamente y eliminar prueba
    sock = socket()
    sock.connect((p.host, p.port))
    client = ClientConnection(sock)
    client.send_command("ping", blocking=False)
    print(client.send_command("echo", value="test"))
    print(client.send_command("echo", value="test2"))
    print(client.send_command("echo", value="test3"))
    print(client.send_command("echo", value=True))
    print(client.send_command("echo", value=False))

    app = QApplication([])
    
    start_window = StartWindow()
    start_logic = StartLogic(client)

    main_window = MainWindow()
    main_logic = MainLogic(client)

    game_window = GameWindow()
    game_logic = GameLogic(client)

    start_window.signal_verify_user.connect(
            start_logic.verify_user
            )

    start_logic.signal_verify_user_reply.connect(
            start_window.verify_user_reply
            )

    start_logic.signal_login.connect(
            main_window.show
            )

    start_logic.signal_login.connect(
            main_logic.join_lobby
            )

    main_window.signal_invite_player.connect(
            main_logic.invite_player
            )

    main_window.signal_prompt_invite_reply.connect(
            main_logic.prompt_invite_reply
            )

    main_logic.signal_update_lobby.connect(
            main_window.update_lobby
            )

    main_logic.signal_invite_player_reply.connect(
            main_window.invite_player_reply
            )

    game_window.signal_next_turn.connect(
            game_logic.next_turn
            )

    game_logic.signal_display_next_turn.connect(
            game_window.display_next_turn
            )
   
    client.signal_prompt_invite.connect(
            main_window.prompt_invite
            )

    client.signal_start_game.connect(
            main_window.hide
            )

    client.signal_start_game.connect(
            main_logic.exit_lobby
            )

    client.signal_start_game.connect(
            game_window.start
            )

    client.signal_end_game.connect(
            game_window.hide
            )

    start_window.show()
    app.exec()
