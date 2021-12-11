from dcconnection import DCConnection
from dccalamar import MarbleGame


class ServerConnection(DCConnection):
    def __init__(self, sock, server):
        super().__init__(sock)
        self.server = server

        self.user = None
        self.name = None
        self.birthday = None

    def run(self):
        try:
            super().run()
        except ConnectionError:
            if self.user is not None:
                print(f"Se ha cerrado la conexión de {self.name}")
                self.server.logout(self.user.name)

    def send_command(self, cmd, blocking=True, **kwargs):
        try:
            return super().send_command(cmd, blocking, **kwargs)
        except ConnectionError:
             if self.user is not None:
                self.server.logout(self.user.name)

    def do_command(self, msg):
        cmd = msg["command"]
        if cmd == "ping":
            print("pong")

        elif cmd == "echo":
            print("echoing", msg["value"])
            return msg["value"]

        elif cmd == "login":
            # TODO hacer esto mejor
            self.name = msg["user"]
            self.birthday = msg["birthday"]

            self.server.login(self.name, self.birthday, self)
            self.user = self.server.users[self.name]
            return True # Para simplificar debuggeo TODO
            #return (user.isalnum() and len(user) >= 1 and len(birthday) == 10 and birthday[2] == "/" and birthday[5] == "/")

        elif cmd == "logout":
            self.server.logout(self.name)
            self.user = None
            self.name = None
            self.birthday = None
            return

        elif cmd == "query-lobby":
            return self.server.query_lobby(self.name)

        elif cmd == "invite":
            invited = msg["invited"]

            accepted = self.user.invite(invited)
            print("respuesta invite recivida", accepted)
            # TODO implementar cancelacion de invitacion
            
            if accepted:
                self.user.exit_lobby()
                self.server.users[invited].exit_lobby()
                self.game = MarbleGame(self.server, self.name, invited)

            return accepted

        elif cmd == "next_turn":
            if self.user.current_game is not None:
                self.user.current_game.player_bet(msg["turn"], self.name, msg["bet_amount"], msg["bet_is_odd"])
                return
            else:
                print("Turno de {self.name} llego cuando el juego ya termino. Ignorando")
                return None
