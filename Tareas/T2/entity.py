import os
from random import choice
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

    def delete_self(self):
        self.parent.entities.remove(self)

    @property
    def current_sprite(self):
        return self.sprite_book[self.sprite_status][self.sprite_cycle]

    @property
    def speed(self):
        return 0

class MovingObstacle(Entity):
    def update(self):
        if self.direction == p.DIR_LEFT:
            self.translate(-1 * self.speed / p.FRAME_RATE, 0)
        elif self.direction == p.DIR_RIGHT:
            self.translate(self.speed / p.FRAME_RATE, 0)
        
        if not self.intersects(self.parent.game_area):
            self.delete_self()

class Car(MovingObstacle):
    def __init__(self, position, direction, parent):
        super().__init__(position, direction, parent)
        self.setSize(p.CAR_SIZE)
        self.sprite_book[p.DIR_RIGHT] = [p.PATH_CAR_RIGHT]
        self.sprite_book[p.DIR_LEFT] = [p.PATH_CAR_LEFT]
        # TODO escoger sprites aleatoriamente

        self.sprite_status = self.direction

    @property
    def speed(self):
        factor = 2/(1+p.PONDERADOR_DIFICULTAD)
        return p.VELOCIDAD_AUTOS * (factor ** (self.parent.current_level - 1))

class Log(MovingObstacle):
    def __init__(self, position, direction, parent):
        super().__init__(position, direction, parent)

        self.setSize(p.LOG_SIZE)
        self.sprite_book["idle"] = [p.PATH_LOG]
        self.sprite_status = "idle"

    @property
    def speed(self):
        factor = 2/(1+p.PONDERADOR_DIFICULTAD)
        return p.VELOCIDAD_TRONCOS * self.parent.skull_bonus * (
                factor ** (self.parent.current_level - 1
                    )) 

class Item(Entity):
    def __init__(self, position, parent):
        super().__init__(position, None, parent)
        self.type = choice(["Calavera", "Corazon", "Moneda", "Reloj"])
        self.layer = 5
        self.setSize(p.ITEM_SIZE)

        self.parent.spawned_item = self
        self.parent.item_spawn_timer.stop()

        self.sprite_book["idle"] = [os.path.join(p.PREFIX_ITEM, self.type + ".png")]
        self.sprite_status = "idle"

    def delete_self(self):
        self.parent.spawned_item = None
        self.parent.item_spawn_timer.start()
        super().delete_self()

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
                return

        for river in self.parent.river_rects:
            if river.contains(self.center()) and self.following_log == None:
                self.die()
                return

        item = self.parent.spawned_item
        if not item is None and self.intersects(item):
            if item.type == "Calavera":
                self.parent.skull_bonus *= p.SKULL_BONUS
            elif item.type == "Corazon":
                self.parent.player_lives += 1
            elif item.type == "Moneda":
                self.parent.player_coins += p.CANTIDAD_MONEDAS
            elif item.type == "Reloj":
                level_time = p.DURACION_RONDA_INICIAL * (
                        p.PONDERADOR_DIFICULTAD ** (self.parent.current_level - 1
                            ))
                self.parent.time_remaining += int(10 * self.parent.time_remaining / level_time)
                # Me tinca que en esta formula deberia haber un +1...
            item.delete_self()

    def die(self):
        self.moveTo(400,600) # TODO : poner numeros adecuados
        self.parent.player_lives -= 1

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

    @property
    def speed(self):
        return p.VELOCIDAD_CAMINAR
