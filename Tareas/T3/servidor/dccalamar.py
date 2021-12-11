from threading import Thread, Condition
from random import shuffle
from parameters import Parameters as p


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
        print('haciendo logout') # TODO
        if name in self.users and self.users[name].current_connection is not None:
            user = self.users[name]
            user.current_game = None
            user.exit_lobby()
            print(f"Usuario {name} se ha desconectado")

    def query_lobby(self, name):
        result = []
        for user in self.lobby.values():
            if user.name != name:
                result.append([user.name, user.available])
        return result

class User:
    def __init__(self, name, birthday, parent):
        self.name = name
        self.birthday = birthday
        self.parent = parent
        self.current_connection = None
        self.current_game = None

        self.available = False

    def join_lobby(self):
        self.available = True
        print(self.parent)
        print(self.parent.lobby)
        self.parent.lobby[self.name] = self
        print(f"Usuario {self.name} se ha unido a la sala de espera")

    def exit_lobby(self):
        if self.name in self.parent.lobby:
            self.available = False
            del self.parent.lobby[self.name]
            print(f"Usuario {self.name} ha salido de la sala de espera")

    def invite(self, invited):
        print(f"Usuario {self.name} invita a {invited} a una partida")
        connection = self.parent.users[invited].current_connection
        return connection.send_command("prompt_invite", inviter=self.name)

    @property
    def is_playing(self):
        return self.current_game is not None

    @property
    def is_loggedin(self):
        return self.current_connection is not None

class MarbleGame(Thread):
    def __init__(self, server, playera, playerb):
        super().__init__(daemon=True)

        self.server = server
        self.players = []
        self.players.append(server.users[playera])
        self.players.append(server.users[playerb])
        shuffle(self.players)

        self.marbles = []
        self.marbles.append(p.STARTING_MARBLES)
        self.marbles.append(p.STARTING_MARBLES)

        self.turn = 0
        
        self.bets_condition = Condition()
        self.bets = []
        self.bets.append(None)
        self.bets.append(None)
        self.is_odd_bet = None

        self.running = True

        self.start()

    def run(self):
        self.players[0].current_game = self
        self.players[0].current_connection.send_command(
                "start_game", blocking=False,
                player=self.players[0].name,
                opponent=self.players[1].name, starter=True, avatar=0
                )
        self.players[1].current_game = self
        self.players[1].current_connection.send_command(
                "start_game", blocking=False,
                player=self.players[1].name,
                opponent=self.players[0].name, starter=False, avatar=1
                )

        while self.running:
            print("Esperando apuestas de jugadores")
            with self.bets_condition:
                self.bets_condition.wait_for(
                        lambda: self.bets[0] is not None and 
                        self.bets[1] is not None and 
                        self.is_odd_bet is not None
                        )

                self.process_turn()

    def process_turn(self):
        betting_player = self.turn % 2
        other_player = (self.turn + 1) % 2
        winner = None

        print(self.turn, betting_player, other_player, self.is_odd_bet)

        if (self.marbles[other_player] % 2 == 1) == self.is_odd_bet:
            winner = betting_player
            loser = other_player
            marbles_gained = self.bets[other_player]
            self.marbles[betting_player] += marbles_gained
            self.marbles[other_player] -= marbles_gained

            print(f"{self.players[betting_player].name} gana la apuesta"
                  f"y obtiene {marbles_gained} canicas de {self.players[other_player].name}")
        else:
            winner = other_player
            loser= betting_player
            marbles_lost = self.bets[betting_player]
            self.marbles[betting_player] -= marbles_lost
            self.marbles[other_player] += marbles_lost

            print(f"{self.players[betting_player].name} perdió la apuesta"
                  f"y le da {marbles_lost} canicas a {self.players[other_player].name}")

        self.bets = [None, None]
        self.is_odd_bet = None

        self.players[winner].current_connection.send_command(
                "reply", blocking=False, replied_command="next_turn",
                value=(True, self.marbles[winner], self.marbles[loser])
                )
        self.players[loser].current_connection.send_command(
                "reply", blocking=False, replied_command="next_turn",
                value=(False, self.marbles[loser], self.marbles[winner])
                )
    
        if self.marbles[0] <= 0:
            self.end_game(1)
        elif self.marbles[1] <= 0:
            self.end_game(0)

        self.turn += 1

    def player_bet(self, turn, player_name, bet_amount, bet_is_odd):
        with self.bets_condition:
            if turn != self.turn:
                print(f"Apuesta invalida de {player_name}. ¿Paquete llegó muy tarde?")
                return

            output = f"{player_name} apostó {bet_amount} canicas"
            if self.players[0].name == player_name:
                self.bets[0] = bet_amount
                if turn % 2 == 0:
                    output += f" a que el oponente apostó {'impar' if bet_is_odd else 'par'}"
                    self.is_odd_bet = bet_is_odd
            else:
                self.bets[1] = bet_amount
                if turn % 2 == 1:
                    output += f" a que el oponente apostó {'impar' if bet_is_odd else 'par'}"
                    self.is_odd_bet = bet_is_odd

            print(output)
            self.bets_condition.notify()

    def end_game(self, winner_index):
        self.running = False
        winner = self.players[winner_index]
        loser = self.players[(winner_index + 1) % 2]

        print(f"{winner.name} ha derrotado a {loser.name} en {self.turn + 1} rondas!")

        winner.current_connection.send_command("end_game", blocking=False, won=True)
        loser.current_connection.send_command("end_game", blocking=False, won=False)
