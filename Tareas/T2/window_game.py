from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap

import parametros as p

class WindowGame(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600) # TODO: cambiar a c/onstantesa

        self.game_area = QWidget(self)
        self.game_area.resize(p.GAME_AREA_SIZE)
        self.game_area.move(0, 100) #TODO quitar esto
    
    def render_level(self, level):
        # En retrospectiva hubiera sido mejor hacer una clase Lane que heredaba de QWidget y usar un layout para esto...
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
                transition_lane.move(0, p.GAME_AREA_SIZE.height() - (1 + current_lane) * p.LANE_WIDTH)

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
        # TODO render stuff
        pass