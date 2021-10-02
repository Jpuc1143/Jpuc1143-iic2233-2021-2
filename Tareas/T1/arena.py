from copy import copy
from random import choice, sample, random

import parametros as p 


class Arena:
    def __init__(self, name, difficulty, risk, parent):
        self.name = name
        self.risk = risk
        self.difficulty = difficulty
        self.player_tribute = None
        self.game_over = False
        self.parent = parent

        self.time = 0
        self.environment_cycle = [environment for environment in self.parent.available_environments.values()]

        self.tributes = dict()
        self.death_list = []

    @property
    def tributes_alive(self):
        return {tribute.name: tribute for tribute in self.tributes.values() if tribute.is_alive}

    @property
    def current_environment(self):
        return self.environment_cycle[self.time % 3]

    @property
    def next_environment(self):
        return self.environment_cycle[(self.time + 1) % 3]

    @property
    def tributes_remaining(self):
        return len(self.tributes_alive)

    def let_them_fight(self):
        encounter_number = int(self.risk * self.tributes_remaining // 2)

        print("Los tributos comienzan a pelear!")
        for encounter in range(encounter_number):
            attacker_gen = [tribute for tribute in self.tributes_alive.values()
                            if tribute != self.player_tribute]
            attacker = choice(attacker_gen)
            defender = choice(list(filter(lambda x: x != attacker, self.tributes_alive.values())))

            attacker.attack(defender)

    def do_random_event(self):
        damage = self.current_environment.damageDealt()

        for tribute in self.tributes_alive.values():
            tribute.health -= damage

    def choose_tributes(self):
        # TODO: explicar
        districts = {}
        for tribute in self.parent.available_tributes.values():
            if tribute.name != self.player_tribute.name and tribute.district != self.player_tribute.district:
                if tribute.district in districts:
                    districts[tribute.district].append(tribue)
                else:
                    districts[tribute.district] = [tribute]

        candidate_districts = sample(list(districts.values()), p.PARTICIPANT_NUMBER-1)
        tributes = {self.player_tribute.name: self.player_tribute}
        for districts in candidate_districts:
            tribute = choice(districts)
            tribute.arena = self
            tributes[tribute.name] = tribute

        self.tributes = tributes

    def simulate(self):
        self.let_them_fight()
        if random() <= p.PROBABILIDAD_EVENTO:
            self.do_random_event()
  
        if self.tributes_remaining < 2 or not self.player_tribute.is_alive:
            self.closing_ceremony()
            return False

        self.time += 1

        return True

    def closing_ceremony(self):
        print("")
        if self.tributes_remaining == 0:
            print("Vaya, parece que todos los tributos que quedaban murieron al mismo tiempo")
            print("No hay ganador en estos juegos")
            print("Que desastre...\n")
            start = 1
        else:
            start = 2
            if self.player_tribute.is_alive:
                print("Winner Winner, Chicken Dinner!")
                winner = self.player_tribute
            else:
                print("Has sido derrotado..")
                winner = choice(list(self.tributes_alive.values()))
                # TODO: anadir al death list los que quedan vivos

            print(f"El ganador del DCCapitolio es {winner.name}!\n")

        print("In Memoriam (Hora de Muerte):")
        for number, tribute in enumerate(reversed(self.death_list), start=start):
            print(f"{number}. {tribute[0].name} ({tribute[1]})")

    def __str__(self):
        output = f'Arena "{self.name}"\n'\
                 f"Riesgo: {self.risk}\n"\
                 f"Dificultad: {self.difficulty}\n"\
                 f"Ambiente Actual: {self.current_environment.name}\n"\
                 f"Próximo ambiente: {self.next_environment.name}\n"\
                 f"Horas transcurridas: {self.time}\n"\
                 f"Tributos Vivos:\n"

        for tribute in self.tributes_alive.values():
            if tribute == self.player_tribute:
                output += f"{tribute.name} (tú): {tribute.health}\n"
            else:
                output += f"{tribute.name}: {tribute.health}\n"

        return output
