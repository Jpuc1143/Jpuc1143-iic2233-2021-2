class DCCalamar:
    def __init__(self):
        # TODO: thread safety
        self.users = dict()
        self.lobby = dict()

    def login(self, name, birthday, connection):
        if name not in self.users:
            print(f"Creando nuevo usuario {name}")
            self.users[name] = User(name, birthday, self)
        self.users[name].current_connection = connection
        # TODO revisar que el usuario no este loggeado primero
        print(f"Usuario {name} ha ingresado con cumpleaños {birthday}")

        self.users[name].join_lobby()

    def logout(self, name):
        if name in self.users:
            self.users[name].current_connection = None
            print(f"Usuario {name} se ha desconectado")

class User:
    def __init__(self, name, birthday, parent):
        self.name = name
        self.birthday = birthday
        self.parent = parent
        self.current_connection = None

        self.available = False

    def join_lobby(self):
        self.available = True
        print(self.parent)
        print(self.parent.lobby)
        self.parent.lobby[self.name] = self
        print(f"Usuario {self.name} se ha unido a la sala de espera")

    def exit_lobby(self):
        self.available = False
        del self.parent.lobby[self.name]
        print(f"Usuario {self.name} ha salido de la sala de espera")

    def invite(self, invited):
        print(f"Usuario {self.name} invita a {invited} a una partida")
        connection = self.parent.users[invited].current_connection
        return connection.send_command("prompt_invite", inviter=self.name)

    @property
    def is_loggedin(self):
        return self.current_connecton is not None
