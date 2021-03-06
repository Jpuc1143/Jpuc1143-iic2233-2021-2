from random import choice, sample, random

from tribute import Tribute
import parametros as p


class Arena:
    def __init__(self, name, difficulty, risk, parent):
        self.name = name
        self.risk = risk
        self.difficulty = difficulty
        self.player_tribute = None
        self.parent = parent

        self.time = 0
        self.environment_cycle = \
            [environment for environment in self.parent.available_environments.values()]

        self.tributes = dict()
        self.death_list = []

        self.save_id = None

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
        encounter_number = max(1, int(self.risk * self.tributes_remaining // 2))

        print("Los tributos comienzan a pelear!")
        for encounter in range(encounter_number):
            attacker_gen = [tribute for tribute in self.tributes_alive.values()
                            if tribute != self.player_tribute]
            attacker = choice(attacker_gen)
            defender = choice(list(filter(lambda x: x != attacker, self.tributes_alive.values())))

            attacker.attack(defender, forced=True)

    def do_random_event(self):
        damage = self.current_environment.damageDealt()

        for tribute in self.tributes_alive.values():
            tribute.health -= damage

    def choose_tributes(self):
        # La arena escoje a los demás tributos de acuerdo a sus distritos.
        # Primero encuentra todos los distritos que tengan los tributos, incluyendo distritos
        # que no fueron especificados. Luego elije un tributo de cada distrito hasta que hayan
        # sido seleccionado la cantidad necesaria de tributos para los juegos.

        # Fuente:
        # https://stackoverflow.com/questions/181530/styling-multi-line-conditions-in-if-statements
        # Utilizado para hacer if-statements de multilinea.
        districts = {}
        for tribute in self.parent.available_tributes.values():
            if (tribute.name != self.player_tribute.name and
                    tribute.district != self.player_tribute.district):
                if tribute.district in districts:
                    districts[tribute.district].append(tribute)
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

        print("\nLos tributos sobrevivientes de esta hora son:")
        for tribute in self.tributes_alive.values():
            print(tribute.name)

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
                others = list(filter(lambda x: x != winner, list(self.tributes_alive.values())))
                for time, tribute in enumerate(sample(others, len(others))):
                    self.death_list.append((tribute, time + self.time + 1))
                self.time = self.death_list[-1][1]
            print(f"Después de {self.time + 1} horas de combate...")
            print(f"El ganador del DCCapitolio es {winner.name}!\n")

        print("In Memoriam (Hora de Muerte):")
        for number, tribute in enumerate(reversed(self.death_list), start=start):
            print(f"{number}. {tribute[0].name} ({tribute[1]})")
        print("")

    def serialize(self):
        self_data = ",".join([self.name, str(self.risk), self.difficulty,
                              self.player_tribute.name, str(self.time)])
        environments = ",".join(map(lambda x: x.name, self.environment_cycle))
        tributes = ",".join(self.tributes.keys())
        tributes_dead = ",".join(map(lambda x: f"{x[0].name},{x[1]}", self.death_list))
        tributes_data = ";".join(map(lambda x: x.serialize(), self.tributes.values()))

        output = ";".join([self_data, environments, tributes, tributes_dead, tributes_data])
        return output

    def deserialize(self, data, save_id, parent):
        split_data = data.split(";")

        self_data = split_data[0].split(",")
        self.name = self_data[0]
        self.risk = float(self_data[1])
        self.difficulty = self_data[2]
        player_tribute_name = self_data[3]
        self.time = int(self_data[4])
        self.parent = parent
        self.save_id = save_id

        self.environment_cycle = list(map(lambda x: self.parent.available_environments[x],
                                          split_data[1].split(",")))

        for tribute_data in split_data[4:]:
            tribute_split = tribute_data.split(",")
            tribute = Tribute(tribute_split[:9])
            tribute.arena = self
            self.tributes[tribute_split[0]] = tribute
            for number, item_data in enumerate(tribute_split[9:]):
                if number % 2 == 0:
                    name = item_data
                else:
                    tribute.inventory[name] = (self.parent.available_items[name], int(item_data))

        self.player_tribute = self.tributes[player_tribute_name]

        if split_data[3] != "":
            for number, data in enumerate(split_data[3].split(",")):
                    if number % 2 == 0:
                        death = [self.tributes[data]]
                    else:
                        death.append(int(data))
                        self.death_list.append(death)
                        death = []

    def __str__(self):
        output = f'Arena "{self.name}"\n'\
                 f"Dificultad: {self.difficulty}\n"\
                 f"Ambiente Actual: {self.current_environment.name} "\
                 f"Próximo ambiente: {self.next_environment.name}\n"\
                 f"Horas transcurridas: {self.time}\n\n"\
                 f"Tributos Vivos:\n"

        for tribute in self.tributes_alive.values():
            if tribute == self.player_tribute:
                output += f"{tribute.name} (tú): {tribute.health:.2f}\n"
            else:
                output += f"{tribute.name}: {tribute.health:.2f}\n"

        return output
