from dcconnection import DCConnection


class ServerConnection(DCConnection):
    def __init__(self, sock, server):
        super().__init__(sock)
        self.server = server

        self.name = None
        self.birthday = None

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

            self.server.login(self.name, self.birthday, self.sock)

            return True # Para simplificar debuggeo TODO
            #return (user.isalnum() and len(user) >= 1 and len(birthday) == 10 and birthday[2] == "/" and birthday[5] == "/")

        elif cmd == "query-lobby":
            print(f"Entregando a {self.name} lista de usuarios disponibles")
            return tuple(map(lambda x: (x.name, x.available),self.server.lobby.values()))