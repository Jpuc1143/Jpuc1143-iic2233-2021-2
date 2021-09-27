from abc import ABC, abstractmethod
import parametros.py as p


class Object(ABC):
    def __init__(self, name, category, weight):
        self.name = name
        self.category = category
        self.weight = weight
        print("TODO: delet tis")

    @abstractmethod
    def use(self, target):
        pass


class Consumable(Object):
    def use(self, target):
        target.energy += p.AUMENTAR_ENERGIA


class Weapon(Object):
    def use(self, target):
        target.strength *= p.PONDERADOR_AUMENTAR_FUERZA * risk + 1
        # TODO: remplazar risk con el riesgo de la arena


class SpecialObject(Weapon, Consumable):
    def use(self, target):
        Consumable.use(self, target)
        Weapon.use(self, target)
        # TODO: implementar el resto de la funcion cuando se aclare que hay que hacer en los issues
