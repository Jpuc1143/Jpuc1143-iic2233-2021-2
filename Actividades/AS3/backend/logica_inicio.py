from PyQt5.QtCore import QObject, pyqtSignal

import parametros as p


class LogicaInicio(QObject):

    senal_respuesta_validacion = pyqtSignal(tuple)
    senal_abrir_juego = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def comprobar_contrasena(self, credenciales):
        success = False
        if credenciales[1].casefold() == p.CONTRASENA.casefold():
            self.senal_abrir_juego.emit(credenciales[0])
            success = True

        self.senal_respuesta_validacion.emit((credenciales[1], success))
