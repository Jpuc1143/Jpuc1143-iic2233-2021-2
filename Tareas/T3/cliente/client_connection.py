from dcconnection import DCConnection


class ClientConnection(DCConnection):
    def __init__(self, sock):
        super().__init__(sock)

    def do_command(self, cmd):
        raise Exception("you done goofed")
