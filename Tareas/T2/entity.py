import os
from PyQt5.QtCore import QRectF, Qt

import parametros as p

class Entity(QRectF):

    def __init__(self, position, direction, parent):
        super().__init__()
        self.parent = parent
        self.parent.entities.append(self)

        self.moveTo(position)
        self.direction = direction

        self.sprite_book = dict()
        self.sprite_status = None
        self.sprite_cycle = 0
        
        self.layer = 0

    def update(self):
        pass

    @property
    def current_sprite(self):
        return self.sprite_book[self.sprite_status][self.sprite_cycle]

    @property
    def speed(self):
        return 50  # TODO: velocidad dinamica


class MovingObstacle(Entity):
    def update(self):
        if self.direction == p.DIR_LEFT:
            self.translate(-1 * self.speed / p.FRAME_RATE, 0)
        elif self.direction == p.DIR_RIGHT:
            self.translate(self.speed / p.FRAME_RATE, 0)
        
        if not self.intersects(self.parent.game_area):
            self.delete_self()

    def delete_self(self):
        self.parent.entities.remove(self)


class Car(MovingObstacle):
    def __init__(self, position, direction, parent):
        super().__init__(position, direction, parent)
        self.setSize(p.CAR_SIZE)
        self.sprite_book[p.DIR_RIGHT] = [p.PATH_CAR_RIGHT]
        self.sprite_book[p.DIR_LEFT] = [p.PATH_CAR_LEFT]
        # TODO escoger sprites aleatoriamente

        self.sprite_status = self.direction

class Log(MovingObstacle):
    def __init__(self, position, direction, parent):
        super().__init__(position, direction, parent)

        self.setSize(p.LOG_SIZE)
        self.sprite_book["idle"] = [p.PATH_LOG]
        self.sprite_status = "idle"

class Frog(Entity):
    def __init__(self, position, direction, color, parent):
        super().__init__(position, direction, parent)

        self.setSize(p.FROG_SIZE)
        self.layer = 10

        self.following_log = None

        self.sprite_status = "idle"

        self.sprite_book["idle"] = [os.path.join(p.PREFIX_FROG, color, f"still.png")]
        animations = ["up", "down", "right", "left"]
        for animation in animations:
            self.sprite_book[animation] = []
            for index in range(1, 4):
                self.sprite_book[animation].append(os.path.join(
                        p.PREFIX_FROG, color, f"{animation}_{index}.png"
                        ))

    def update(self):
        self.update_movement()

        self.following_log = None
        for log in filter(lambda x: isinstance(x, Log), self.parent.entities):
            if log.contains(self.center()):
                self.following_log = log

        if not self.following_log is None:
            if self.following_log.direction == p.DIR_RIGHT:
                self.move(self.following_log.speed / p.FRAME_RATE, 0)
            else:
                self.move(-1 * self.following_log.speed / p.FRAME_RATE, 0)

        for car in filter(lambda x: isinstance(x, Car), self.parent.entities):
            if car.intersects(self):
                self.die()

    def die(self):
        self.moveTo(400,0)
        # TODO

    def move(self, x, y):
        self.translate(x, y)

        if self.right() > p.GAME_AREA_SIZE.width():
            self.translate(p.GAME_AREA_SIZE.width() - self.right(), 0)
        if self.left() < 0:
            self.translate(-self.left(), 0)
        if self.bottom() > p.GAME_AREA_SIZE.height():
            self.translate(0, p.GAME_AREA_SIZE.height() - self.bottom())
        if self.top() < 0:
            pass # TODO win

        next_log = None
        for log in filter(lambda x: isinstance(x, Log), self.parent.entities):
            if log.contains(self.center()):
                next_log = log

        for river in self.parent.river_rects:
            if river.contains(self.center()):
                if next_log == None:
                    self.translate(-x, -y)

    def update_movement(self):
        keyboard = self.parent.keyboard

        if keyboard[Qt.Key_W]:
            self.move(0, -1*self.speed / p.FRAME_RATE)

            if self.direction == p.DIR_UP:
                self.sprite_cycle += 1
                if self.sprite_cycle > 2:
                    self.sprite_cycle = 0
            else:
                self.sprite_cycle = 0
            self.direction = p.DIR_UP
            self.sprite_status = "up"

        if keyboard[Qt.Key_S]:
            self.move(0, self.speed / p.FRAME_RATE)

            if self.direction == p.DIR_DOWN:
                self.sprite_cycle += 1
                if self.sprite_cycle > 2:
                    self.sprite_cycle = 0
            else:
                self.sprite_cycle = 0
            self.direction = p.DIR_DOWN
            self.sprite_status = "down"

        if keyboard[Qt.Key_A]:
            self.move(-1*self.speed / p.FRAME_RATE, 0)

            if self.direction == p.DIR_LEFT:
                self.sprite_cycle += 1
                if self.sprite_cycle > 2:
                    self.sprite_cycle = 0
            else:
                self.sprite_cycle = 0
            self.direction = p.DIR_LEFT
            self.sprite_status = "left"

        if keyboard[Qt.Key_D]:
            self.move(self.speed / p.FRAME_RATE, 0)

            if self.direction == p.DIR_RIGHT:
                self.sprite_cycle += 1
                if self.sprite_cycle > 2:
                    self.sprite_cycle = 0
            else:
                self.sprite_cycle = 0
            self.direction = p.DIR_RIGHT
            self.sprite_status = "right"


