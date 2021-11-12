from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap

import parametros as p

class WindowGame(QWidget):

    signal_game_key_down = pyqtSignal(int)
    signal_game_key_up = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600) # TODO: cambiar a c/onstantesa

        self.game_area = QWidget(self)
        self.game_area.resize(p.GAME_AREA_SIZE)
        self.game_area.move(0, 100) #TODO quitar esto

        self.sprites = []

    def render_level(self, level):
        # En retrospectiva hubiera sido mejor hacer una clase Lane que
        # heredaba de QWidget y usar un layout para esto...
        # Pero ya es muy tarde...

        starting_area = QLabel(self.game_area)
        starting_area.setScaledContents(True)
        starting_area.setPixmap(QPixmap(p.PATH_GRASS))
        starting_area.resize(p.LANE_LENGTH, p.LANE_WIDTH)
        starting_area.move(0, p.GAME_AREA_SIZE.height() - p.LANE_WIDTH)
        
        current_lane = 1
        for index, lane_type in enumerate(level):
            lane = QLabel(self.game_area)
            lane.setScaledContents(True)

            if index != 0 and level[index - 1] != lane_type:
                transition_lane = QLabel(self.game_area)
                transition_lane.setScaledContents(True)
                transition_lane.setPixmap(QPixmap(p.PATH_GRASS))
                transition_lane.resize(p.LANE_LENGTH, p.LANE_WIDTH)
                transition_lane.move(0, 
                        p.GAME_AREA_SIZE.height() - (1 + current_lane) * p.LANE_WIDTH)

                current_lane += 1

            if lane_type == "H":
                lane.setPixmap(QPixmap(p.PATH_HIGHWAY))

            elif lane_type == "R":
                lane.setPixmap(QPixmap(p.PATH_RIVER))
                
            else:
                raise TypeError("Not a valid lane type")

            lane.resize(p.LANE_LENGTH, 3 * p.LANE_WIDTH)
            lane.move(0, p.GAME_AREA_SIZE.height() - (3 + current_lane) * p.LANE_WIDTH)

            current_lane += 3
        
        if current_lane + 1 < p.LANE_NUM:
            transition_lane = QLabel(self.game_area)
            transition_lane.setScaledContents(True)
            transition_lane.setPixmap(QPixmap(p.PATH_GRASS))
            transition_lane.resize(p.LANE_LENGTH, p.LANE_WIDTH)
            transition_lane.move(0, p.GAME_AREA_SIZE.height() - (1 + current_lane) * p.LANE_WIDTH)

        goal_area = QLabel(self.game_area)
        goal_area.setScaledContents(True)
        goal_area.setPixmap(QPixmap(p.PATH_GRASS))
        goal_area.resize(p.LANE_LENGTH, p.LANE_WIDTH)

        self.show()

    def render(self, data):
        # TIL: la funcion de map no se hace cuando se llama, sino solo cuando se itera
        list(map(lambda x: x.deleteLater(), self.sprites))  
        self.sprites = []

        self.entities = data[0]
        for entity in self.entities:
            sprite = QLabel("car",self.game_area)
            sprite.setPixmap(QPixmap(entity.current_sprite))
            sprite.setScaledContents(True)
            sprite.setGeometry(entity.toRect())
            sprite.show()
            self.sprites.append(sprite)

    def keyPressEvent(self, event):
        self.signal_game_key_down.emit(event.key())

    def keyReleaseEvent(self, event):
        self.signal_game_key_up.emit(event.key())
