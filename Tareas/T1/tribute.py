from copy import copy
from random import choice

import parametros as p


class Tribute:
    def __init__(self, stats):
        self.name = stats[0]
        self.district = stats[1]
        self.age = int(stats[2])
        self._health = float(stats[3])
        self._energy = float(stats[4])
        self.agility = int(stats[5])
        self.strength = int(stats[6])
        self.intelligence = int(stats[7])
        self.popularity = int(stats[8])

        self.inventory = {}
        self.arena = None

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
        elif value <= 0:
            self._health = 0
            print(f"{self.name} ha sido eliminad@!")
            self.arena.death_list.append((self, self.arena.time))
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
        for item, qty in self.inventory.values():
            acc += item.weight
        return acc

    def attack(self, target, forced=False):
        if self.energy >= p.ENERGIA_ATACAR or forced:
            numerator = 60*self.strength+40*self.agility+40*self.intelligence-30*self.weight
            damage = min(90, max(5, (numerator/self.age)))
            print(f"{self.name} atacó a {target.name} por {damage:0.2f} de daño")
            if target.health <= damage:
                print(f"{self.name} asesina a sangre fría a {target.name} "
                      f"y gana {p.POPULARIDAD_ATACAR} popularidad")
                self.popularity += p.POPULARIDAD_ATACAR

            target.health -= damage
            if not forced:
                self.energy -= p.ENERGIA_ATACAR
                print(f"Se gasto {p.ENERGIA_ATACAR} de energia, quedandose con {self.energy}")
        else:
            print(f"{self.name} no tiene suficiente energia para atacar...")

    def use_item(self, item):
        try:
            if self.inventory[item.name][1] > 0:
                item.use(self)
                qty = self.inventory[item.name][1] - 1
                self.inventory[item.name] = (item, qty)
                if self.inventory[item.name][1] == 0:
                    del self.inventory[item.name]
            else:
                raise ValueError

        except (KeyError, ValueError):
            # Fuente:
            # https://stackoverflow.com/questions/6470428/
            # catch-multiple-exceptions-in-one-line-except-block
            # Utilizado para capturar más de un tipo de excepción.
            print("ERROR: f{self.name} no tiene {item.name} en su inventario")
            # La estructura del programa no deberia dejar pasar esto, pero por si acaso...

    def request_item(self):
        if self.popularity >= p.POPULARIDAD_PEDIR:
            self.popularity -= p.POPULARIDAD_PEDIR
            item = copy(choice(list(self.arena.parent.available_items.values())))

            if item.name in self.inventory:
                qty = self.inventory[item.name][1] + 1
                self.inventory[item.name] = (item, qty)
            else:
                self.inventory[item.name] = (item, 1)

            print(f"La popularidad de {self.name} causo que los patrocinadores "
                  f"le entregaran un {item.name}!")
            print(f"Sin embargo, perdiste {p.POPULARIDAD_PEDIR} popularidad "
                  f"y te quedan {self.popularity}")
            return True

        else:
            print(f"Como {self.name} no es lo suficientemente popular, "
                  f"nadie le patrocino un objeto...")
            return False

    def heroic_action(self):
        if self.energy >= p.ENERGIA_ACCION_HEROICA:
            self.energy -= p.ENERGIA_ACCION_HEROICA
            self.popularity += p.POPULARIDAD_ACCION_HEROICA
            print(f"{self.name} gana {p.POPULARIDAD_ACCION_HEROICA} "
                  f"popularidad debido a su heroismo")
            print(f"gastando {p.ENERGIA_ACCION_HEROICA} de energia y quedando con {self.energy}")
            return True
        else:
            print(f"{self.name} no tiene suficiente energia para ser un heroe...")
            return False

    def bakugan_mode(self):
        self.energy += p.ENERGIA_BOLITA
        print(f"{self.name} se sienta en una esquina y hace su mejor imitación de un Bakugan")
        print(f"Se recupera {p.ENERGIA_BOLITA} y ahora tienes {self.energy}")

    def serialize(self):
        self_data = ",".join([self.name, self.district, str(self.age), str(self.health),
                             str(self.energy), str(self.agility), str(self.strength),
                             str(self.intelligence), str(self.popularity)])
        inventory_data = ",".join(map(lambda x: x[0].name + "," + str(x[1]),
                                      self.inventory.values()))

        return self_data + "," + inventory_data

    def __str__(self):
        output = ""
        if self.arena is None:
            output += f"{self.name}, tributo del distrito {self.district}\n"
        else:
            output += f"{self.name}, tributo del distrito {self.district} "
            output += f"participando en {self.arena.name}\n"
        output += f"Edad: {self.age}\n"
        output += f"Vida: {self.health:.2f} Energia: {self.energy} "
        output += f"Popularidad: {self.popularity}\n"
        output += f"Fuerza: {self.strength:.2f} Agilidad: {self.agility} "
        output += f"Inteligencia: {self.intelligence}\n"

        inventory_data = []
        for item in self.inventory.values():
            inventory_data.append(f"{item[0].name} ({item[1]})")

        output += "Inventario: " + ", ".join(inventory_data) + "\n"
        output += f"Peso Total: {self.weight}\n"
        return output
