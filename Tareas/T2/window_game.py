from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QPushButton
from PyQt5.QtGui import QPixmap

from queue import PriorityQueue

import parametros as p

class WindowGame(QWidget):

    signal_game_key_down = pyqtSignal(int)
    signal_game_key_up = pyqtSignal(int)

    signal_pause_game = pyqtSignal()
    signal_resume_game = pyqtSignal()
    signal_quit_game = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600) # TODO: cambiar a c/onstantesa

        self.game_area = QWidget(self)
        self.game_area.setMinimumSize(p.GAME_AREA_SIZE)
        self.game_area.resize(p.GAME_AREA_SIZE)

        self.sprites = []

        # Barra de estado

        life_image = QLabel()
        life_image.setScaledContents(True)
        life_image.setPixmap(QPixmap(p.PATH_LIFE))
        self.life_counter = QLabel("num")

        time_image = QLabel()
        time_image.setScaledContents(True)
        time_image.setPixmap(QPixmap(p.PATH_CLOCK))
        self.time_counter = QLabel("num")

        coin_image = QLabel()
        coin_image.setScaledContents(True)
        coin_image.setPixmap(QPixmap(p.PATH_COIN))
        self.coin_counter = QLabel("num")

        self.score_counter = QLabel()

        self.level_counter = QLabel("lv1")

        self.quit_button = QPushButton("Salir")
        self.quit_button.clicked.connect(self.quit_game)
        self.pause_button = QPushButton("Pausa")
        self.pause_button.clicked.connect(self.toggle_pause)

        data = [
                [
                    life_image, self.life_counter, time_image,
                    self.time_counter, coin_image, self.coin_counter
                ],
                [QLabel("Score:"), self.score_counter],
                [QLabel("Level:"), self.level_counter, self.quit_button, None, self.pause_button, None]
                ]

        status_bar = QGroupBox(self)
        status_bar_layout = QHBoxLayout(status_bar)
        for frame_data in data:
            frame = QFrame(status_bar)
            layout = QGridLayout(frame)
            for index, widget in enumerate(frame_data):
                if widget is None:
                    continue
                layout.addWidget(widget, index * len(frame_data)/ 2, index % 2)
            status_bar_layout.addWidget(frame)

        vbox = QVBoxLayout(self)
        vbox.addWidget(status_bar)
        vbox.addWidget(self.game_area)

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
        # Barra de Estado
        self.life_counter.setText(str(data[1]))
        self.life_counter.repaint()
        self.time_counter.setText(str(data[2]))
        self.time_counter.repaint()
        self.coin_counter.setText(str(data[3]))
        self.coin_counter.repaint()
        self.score_counter.setText(str(data[4]))
        self.score_counter.repaint()
        self.level_counter.setText(str(data[5]))
        self.level_counter.repaint()

       # TIL: la funcion de map no se hace cuando se llama, sino solo cuando se itera
        list(map(lambda x: x.deleteLater(), self.sprites))  
        self.sprites = []

        self.entities = data[0]
        layered_entities = []
        for entity in self.entities:
            sprite = QLabel("car",self.game_area)
            sprite.setPixmap(QPixmap(entity.current_sprite))
            sprite.setScaledContents(True)
            sprite.setGeometry(entity.toRect())
            sprite.show()

            self.sprites.append(sprite)
            layered_entities.append((entity.layer, sprite))

        list(map(lambda x: x[1].raise_(), sorted(layered_entities, key=lambda x: x[0])))
        # El uso de raise_() en vez de raise() se debe al leer QtWidgets.pyi en /usr/lib/

 

    def keyPressEvent(self, event):
        self.signal_game_key_down.emit(event.key())
        if event.key() == Qt.Key_P:
            self.toggle_pause()

    def keyReleaseEvent(self, event):
        self.signal_game_key_up.emit(event.key())

    def toggle_pause(self):
        if self.pause_button.text() == "Pausa":
            self.pause_button.setText("Continuar")
            self.signal_pause_game.emit()
        else:
            self.pause_button.setText("Pausa")
            self.signal_resume_game.emit()

    def quit_game(self):
        self.signal_quit_game.emit()
