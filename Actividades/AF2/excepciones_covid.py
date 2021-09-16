class RiesgoCovid(Exception):

    def __init__(self, sintoma, nombre_invitade):
        self.sintoma = sintoma
        self.nombre_invitade = nombre_invitade

    def alerta_de_covid(self):
        if self.sintoma == "dolor_cabeza":
            print(f"{self.nombre_invitade} tiene dolor de cabeza "
                  "y tiene prohibido entrar a DCCarrete")
        else:
            print(f"{self.nombre_invitade} tiene {self.sintoma} "
                  "y tiene prohibido entrar a DCCarrete")
