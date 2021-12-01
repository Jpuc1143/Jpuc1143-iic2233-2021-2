from dccalamar import DCCalamar


class Client(DCCalamar):
    def __init__(self, sock):
        super().__init__(sock)
        # TODO hacer login ???

    def do_command(self, cmd):
        raise Exception("you done goofed")
