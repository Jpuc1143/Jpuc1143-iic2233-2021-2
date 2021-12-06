from dcconnection import DCConnection


class ServerConnection(DCConnection):
    def do_command(self, msg):
        cmd = msg["command"]
        if cmd == "ping":
            print("pong")
        elif cmd == "echo":
            print("echoing", msg["value"])
            return msg["value"]
        
        elif cmd == "login":
            print("Loggin in", msg["user"], "with", msg["birthday"])
            # TODO hacer esto mejor
            user = msg["user"]
            birthday = msg["birthday"]
            return (user.isalnum() and len(user) >= 1 and len(birthday) == 10 and birthday[2] == "/" and birthday[5] == "/")
