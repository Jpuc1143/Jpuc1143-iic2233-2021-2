import random
import parametros as p

class Mascota:
    def __init__(self, nombre, raza, dueno,
                 saciedad, entretencion):
        self.nombre = nombre
        self.raza = raza
        self.dueno = dueno
        
        # Los siguientes valores están en %.
        self._saciedad = saciedad
        self._entretencion = entretencion

    @property
    def saciedad(self):
        return self._saciedad

    @saciedad.setter
    def saciedad(self, valor):
        if valor > 100:
            self._saciedad = 100
        elif valor < 0:
            self._saciedad = 0
        else:
            self._saciedad = valor

    @property
    def entretencion(self):
        return self._entretencion

    @entretencion.setter
    def entretencion(self, valor):
        if valor > 100:
            self._entretencion = 100
        elif valor < 0:
            self._entretencion = 0
        else:
            self._entretencion = valor

    @property
    def satisfaccion(self):
        return (self.saciedad//2 + self.entretencion//2)
    
    def comer(self, comida):
        if random.random() < comida.probabilidad_vencer:
            self.saciedad -= comida.calorias
            print(f"La comida estaba vencida y {self.nombre} vomitó {comida.calorias} calorías :(")
        else:
            self.saciedad += comida.calorias
            print(f"{self.nombre} se alimento con {comida.nombre} de {comida.calorias} calorías :)")

    def pasear(self):
        self.entretencion += p.ENTRETENCION_PASEAR
        self.saciedad += p.SACIEDAD_PASEAR
    
    def __str__(self):
        return f"Nombre: {self.nombre}\n"\
            f"Saciedad: {self.saciedad}%\n"\
            f"Entretención: {self.entretencion}%\n"\
            f"Satisfacción: {self.satisfaccion}%\n"\


class Perro(Mascota):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.especie = "PERRO"
    
    def saludar(self):
        print("Woof woof!")

class Gato(Mascota):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.especie = "GATO"

    def saludar(self):
        print("miauu")

class Conejo(Mascota):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.especie = "CONEJO"

    def saludar(self):
        print("*Sonidos de DCConejo*")
