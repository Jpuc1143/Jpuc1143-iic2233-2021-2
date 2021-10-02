from abc import ABC, abstractmethod
from random import choice

import parametros as p


class Environment:
    @abstractmethod
    def __init__(self, events):
        self.events = events

        self.humidity = 0
        self.wind = 0
        self.rain = 0
        self.clouds = 0

    def damageDealt(self):
        event = choice(list(self.events.items()))
        print(f"La arena esta siendo afectada por un/una {event[0]}!")
        damage =  max(5, (0.4*self.humidity+0.2*self.wind+0.1*self.rain+0.3*self.clouds + event[1])/5)
        print(f"Todos los tributos sufren {damage} puntos de daño")
        return damage

class Beach(Environment):
    def __init__(self, events):
        super().__init__(events)
        self.name = "playa"
        self.humidity = p.HUMEDAD_PLAYA
        self.wind = p.VELOCIDAD_VIENTOS_PLAYA


class Mountain(Environment):
    def __init__(self, events):
        super().__init__(events)
        self.name = "montaña"
        self.rain = p.PRECIPITACIONES_MONTANA
        self.clouds = p.NUBOSIDAD_MONTANA


class Forest(Environment):
    def __init__(self, events):
        super().__init__(events)
        self.name = "bosque"
        self.wind = p.VELOCIDAD_VIENTOS_BOSQUE
        self.rain = p.PRECIPITACIONES_BOSQUE
