from random import choice, randint

from PyQt5.QtCore import pyqtSignal, QObject, QPoint, QTimer, QRectF, QSizeF, Qt

import parametros as p
from entity import Car, Log, Item, Frog
from keyboard_status import Keyboard


class LogicGame(QObject):

    signal_render = pyqtSignal(list)
    signal_render_level= pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.keyboard = Keyboard()

        self.frame_timer = QTimer()
        self.frame_timer.setInterval(int(1000 / p.FRAME_RATE))
        self.frame_timer.timeout.connect(self.update_game)

        self.level_timer = QTimer()
        self.level_timer.setInterval(1000)
        self.level_timer.timeout.connect(self.level_timer_tick)

        self.car_spawn_timer = QTimer()
        self.car_spawn_timer.setInterval(p.TIEMPO_AUTOS * 1000)
        self.car_spawn_timer.timeout.connect(self.spawn_car)

        self.log_spawn_timer = QTimer()
        self.log_spawn_timer.setInterval(p.TIEMPO_TRONCOS * 1000)
        self.log_spawn_timer.timeout.connect(self.spawn_log)

        self.item_spawn_timer = QTimer()
        self.item_spawn_timer.setInterval(p.TIEMPO_OBJETO * 1000)
        self.item_spawn_timer.timeout.connect(self.spawn_item)

        self.game_area = QRectF()
        self.game_area.setSize(QSizeF(p.GAME_AREA_SIZE))

    def start_game(self):
        self.time_remaining = p.DURACION_RONDA_INICIAL

        self.player_lives = p.VIDAS_INICIO
        self.score = 0
        self.current_level = 1
        self.player_coins = 0
        self.spawned_item = None
        self.skull_bonus = 1

        self.entities = list()  # No optimo. ¿Por qué Python no tiene linked lists en stdlib?

        self.generate_level()
        
        self.spawn_car()
        self.spawn_log()
        self.player = Frog(QPoint(p.LANE_LENGTH/2, self.lane_to_pos(0)), p.DIR_UP, p.FROG_SKIN_0, self)

        self.update_game()
        self.resume_game()
        
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

        current_lane = 1
        self.area_layout = list(map(lambda x: [x, None, []], level))
        for index, area in enumerate(self.area_layout):
            if index != 0 and area[0] != self.area_layout[index-1][0]:
                current_lane += 1

            area[1] = current_lane
            if area[0] == "H":
                for index in range(3):
                    area[2].append(choice([p.DIR_LEFT, p.DIR_RIGHT]))
            else:
                if index != 0 and self.area_layout[index-1][0] == area[0]:
                    area[2].append(self.area_layout[index-1][2][1])
                else:
                    area[2].append(choice([p.DIR_LEFT, p.DIR_RIGHT]))
                if area[2][0] == p.DIR_LEFT:
                    area[2].append(p.DIR_RIGHT)
                    area[2].append(p.DIR_LEFT)
                else:
                    area[2].append(p.DIR_LEFT)
                    area[2].append(p.DIR_RIGHT)

            current_lane += 3
            
        self.river_rects = []
        for area in self.area_layout:
            if area[0] == "R":
                self.river_rects.append(QRectF(
                    0, self.lane_to_pos(area[1] + 2),
                    p.LANE_LENGTH, 3 * p.LANE_WIDTH
                        ))

    def next_level(self):
        pass

    def resume_game(self):
        self.frame_timer.start()
        self.level_timer.start()
        self.car_spawn_timer.start()
        self.log_spawn_timer.start()
        if self.spawned_item is None:
            self.item_spawn_timer.start()

    def pause_game(self):
        self.frame_timer.stop()
        self.level_timer.stop()
        self.car_spawn_timer.stop()
        self.log_spawn_timer.stop()

    def update_game(self):
        for entity in self.entities:
            entity.update()

        if self.player_lives <= 0 or self.time_remaining <= 0:
            self.lose_game()
            return

        if self.player.top() == self.game_area.top():
            self.win_game()
            return

        self.signal_render.emit([
            self.entities, self.player_lives, self.time_remaining,
            self.player_coins, self.score, self.current_level
            ])

    def level_timer_tick(self):
        self.time_remaining -= 1
        if self.time_remaining <= 0:
            self.level_timer.stop()

    def spawn_car(self):
        for highway in filter(lambda x: x[0] == "H", self.area_layout):
            lane = randint(0, 2)
            direction = highway[2][lane]
            car = Car(QPoint(p.GAME_AREA_SIZE.width(), self.lane_to_pos(highway[1] + lane)), direction, self)
            if direction == p.DIR_RIGHT:
                car.moveRight(0)

    def spawn_log(self):
        for river in filter(lambda x: x[0] == "R", self.area_layout):
            lane = randint(0, 2)
            direction = river[2][lane]
            log = Log(QPoint(p.GAME_AREA_SIZE.width(), self.lane_to_pos(river[1] + lane)), direction, self)
            if direction == p.DIR_RIGHT:
                log.moveRight(0)

    def spawn_item(self):
        available_lanes = set(range(p.LANE_NUM))
        for area in filter(lambda x: x[0] == "R", self.area_layout):
            for index in range(3):
                available_lanes.remove(area[1] + index)
        available_lanes.discard(0)
        available_lanes.discard(p.LANE_NUM - 1)
        available_lanes.discard(p.LANE_NUM - 2)
        lane = choice(list(available_lanes))

        x_pos = randint(0, p.LANE_LENGTH - p.ITEM_SIZE.width())
        y_pos = self.lane_to_pos(lane) + p.LANE_WIDTH/2 - p.ITEM_SIZE.height()/2
        Item(QPoint(x_pos, y_pos), self)

    def lane_to_pos(self, lane):
        return p.GAME_AREA_SIZE.height() - (1 + lane) * p.LANE_WIDTH

    def key_down(self, key):
        self.keyboard[key] = True

    def key_up(self, key):
        self.keyboard[key] = False

    def win_game(self):
        self.pause_game()

    def lose_game(self):
        self.pause_game()

    def calculate_level_score():
        return self.current_level * (self.player_lives * 100 + self.time_remaining * 50)
