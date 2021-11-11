from random import choice

from PyQt5.QtCore import pyqtSignal, QObject, QTimer

import parametros as p


class LogicGame(QObject):

    signal_render = pyqtSignal(list)
    signal_render_level= pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.frame_timer = QTimer()
        self.frame_timer.setInterval(int(1 / p.FRAME_RATE))
        self.frame_timer.timeout.connect(self.update_game)

        self.level_timer = QTimer()
        self.level_timer.setInterval(1000)
        self.level_timer.timeout.connect(self.level_timer_tick)

    def start_game(self):
        self.time_remaining = p.DURACION_RONDA_INICIAL

        self.log_speed = p.VELOCIDAD_AUTOS
        self.car_speed = p.VELOCIDAD_TRONCOS

        self.player_lives = p.VIDAS_INICIO

        self.generate_level()
        self.update_game()

    def generate_level(self):
        level = []
        level.append(choice(["H", "R"]))
        level.append(choice(["H", "R"]))
        if level[0] != level[1]:
            level.append(choice(["H", "R"]))
        elif level[0] == "H":
            level.append("R")
        else:
            level.append("H")

        self.signal_render_level.emit(level)

    def next_level(self):
        pass

    def update_game(self):
        # logic updates TODO

        self.signal_render.emit((1,))  # TODO: poner todo lo necesario en el emit

    def level_timer_tick(self):
        self.time_remaining -= 1
        if self.time_remaining <= 0:
            self.level_timer.stop()
