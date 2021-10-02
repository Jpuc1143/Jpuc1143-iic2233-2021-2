from abc import ABC, abstractmethod
import parametros as p


class Item(ABC):
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    @abstractmethod
    def use(self, target):
        pass


class Consumable(Item):
    def __init__(self, name, weight):
        Item.__init__(self, name, weight)
        self.category = "consumible"

    def use(self, target):
        target.energy += p.AUMENTAR_ENERGIA


class Weapon(Item):
    def __init__(self, name, weight):
        Item.__init__(self, name, weight)
        self.category = "arma"

    def use(self, target):
        target.strength *= p.PONDERADOR_AUMENTAR_FUERZA * target.arena.risk + 1


class SpecialItem(Weapon, Consumable):
    def __init__(self, name, weight):
        Item.__init__(self, name, weight)
        self.category = "especial"

    def use(self, target):
        Consumable.use(self, target)
        Weapon.use(self, target)
        target.agility += p.AUMENTAR_AGILIDAD
        target.intelligence += p.AUMENTAR_INGENIO
