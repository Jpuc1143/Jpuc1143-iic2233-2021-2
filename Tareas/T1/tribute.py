import parametros.py as p


class Tribute:
    def __init__(self, stats, arena):
        self.name = stats[0]
        self.district = stats[1]
        self.age = int(stats[2])
        self.health = int(stats[3])
        self.energy = int(stats[4])
        self.agility = int(stats[5])
        self.strength = int(stats[6])
        self.intelligence = int(stats[7])
        self.popularity = int(stats[8])

        self.inventory = []
        self.arena = arena

    @property
    def is_alive(self):
        return self._health != 0

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value > 100:
            self._health = 100
        elif value < 0:
            self._health = 0
        else:
            self._health = value

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        if value > 100:
            self._energy = 100
        elif value < 0:
            self._energy = 0
        else:
            self._energy = value

    @property
    def weight(self):
        acc = 0
        for item, qty in self.inventory:
            acc += item.weight
        return acc

    def attack(self, target, forced=False):
        if self.energy >= p.ENERGIA_ATACAR or forced:
            numerator = 60*self.strength+40*self.agility+40*self.intelligence-30*self.weight
            damage = min(90, max(5, (numerator/self.age)))
            print(f"{self.name} atacó a {target.name} con {damage} de daño")
            if target.health == 0:
                print("{self.name} asesina a sangre fría a {target.name}")
                self.popularity += p.POPULARIDAD_ATACAR

            self.energy -= p.ENERGIA_ATACAR
        else:
            print(f"{self.name} no tiene suficiente energia para atacar...")

    def use_item(self, item):
        try:
            if self.inventory[item.name][1] > 0:
                item.use(self)
                self.inventory[item.name][1] -= 1
                if self.inventory[item.name][1] == 0:
                    del self.inventory[item.name]
            else:
                raise ValueError

        except (KeyError, ValueError):
            # Fuente: https://stackoverflow.com/questions/6470428/catch-multiple-exceptions-in-one-line-except-block
            # Utilizado para capturar más de un tipo de excepción.
            print("ERROR: f{self.name} no tiene {item.name} en su inventario")
            # La estructura del programa no deberia dejar pasar esto, pero por si acaso...

    def request_item(self):
        # item = choice TODO: impementar correctamente
        pass

    def heroic_action(self):
        if self.energy >= p.ENERGIA_ACCION_HEROICA:
            self.energy -= p.ENERGIA_ACCION_HEROICA
            self.popularity += p.POPULARIDAD_ACCION_HEROICA
            print(f"{self.nombre} gana popularidad debido a su heroismo")
        else:
            print(f"{self.nombre} no tiene suficiente energia para ser un heroe...")

    def bakugan_mode(self):
        self.energia += p.ENERGIA_BOLITA
        print(f"{self.nombre} se sienta en una esquina y hace su mejor imitación de un Bakugan")
