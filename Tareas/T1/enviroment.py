from random import choice
import parametros.py as p


class Enviroment:
    def __init__(self, name, events):
        self.name = name
        self.events = events

        self.humidity = 0
        self.wind = 0
        self.rain = 0
        self.clouds = 0

        if name == "playa":
            self.humidity = p.HUMEDAD_PLAYA
            self.wind = p.VELOCIDAD_VIENTOS_PLAYA

        elif name == "montaña":
            self.rain = p.PRECIPITACIONES_MONTANA
            self.clouds = p.NUBOSIDAD_MONTANA

        elif name == "bosque":
            self.wind = p.VELOCIDAD_VIENTOS_BOSQUE
            self.rain = p.PRECIPIACIONES_BOSQUE

    def damageDealt(self):
        event = choice(self.events)
        print(f"Esta occuriendo un {event[0]}!")
        return max(5, (0.4*self.humidity+0.2*self.wind+0.1*self.rain+0.3*self.clouds + event[1])/5)
