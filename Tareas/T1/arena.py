from random import choice


class Arena:
    def __init__(self, risk, difficulty, player_tribute, parent):
        self.risk = risk
        self.difficulty = difficulty
        self.player_tribute = player_tribute
        self.game_over = False
        self.parent = parent

        self.environment_cycle = []
        self._current_enviroment = 0  # TODO: usar lista de ambientes de la clase padre

        self.tributes = dict()  # TODO: obtener tributos de clase padre

    @property
    def tributes_alive(self):
        return {tribute for tribute in self.tributes if tribute.alive}

    @property
    def current_enviroment(self):
        return self.environment_cycle[self._current_enviroment]

    @property
    def tributes_remaining(self):
        return len(self.tributes_alive)

    def let_them_fight(self):
        encounter_number = self.risk * self.tributes_remaining // 2

        print("Los tributos comienzan a pelear!")
        for encounter in range(encounter_number):
            attacker_gen = [tribute for tribute in self.tributes_alive
                            if tribute != self.player_tribute]
            attacker = choice(attacker_gen)
            defender = choice(self.tributes_alive)

            attacker.attack(defender)

    def do_random_event(self):
        damage = self.current_environment.damageDealt()

        for tribute in self.tributes_alive:
            tribute.health -= damage
