from PyQt5.QtCore import QRectF

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

    def update(self):
        pass

    @property
    def current_sprite(self):
        return self.sprite_book[self.sprite_status][self.sprite_cycle]

class MovingObstacle(Entity):
    def update(self):
        if self.direction == p.DIR_LEFT:
            self.translate(-1 * self.speed / p.FRAME_RATE, 0)
        elif self.direction == p.DIR_RIGHT:
            self.translate(self.speed / p.FRAME_RATE, 0)
        
        if not self.intersects(self.parent.game_area):
            self.delete_self()

    def delete_self(self):
        print("self borrado")
        self.parent.entities.remove(self)

    @property
    def speed(self):
        return 50  # TODO: velocidad dinamica

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

