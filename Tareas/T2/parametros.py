import os
from PyQt5.QtCore import QSize, QSizeF, QPoint, Qt

MIN_CARACTERES = 1
MAX_CARACTERES = 12

WINDOW_OFFSET = QPoint(50, 50)

GAME_AREA_SIZE = QSize(800, 910)
FRAME_RATE = 20
ICON_SIZE = QSize(40, 40)

DIR_DOWN = 0
DIR_RIGHT = 1
DIR_UP = 2
DIR_LEFT = 3

LANE_NUM = 13  # 3*3 para los rios y carreteras, 2 para el inicio y fin, y 2 para las transiciones
LANE_LENGTH = GAME_AREA_SIZE.width()
LANE_WIDTH = GAME_AREA_SIZE.height() / LANE_NUM

DURACION_RONDA_INICIAL = 100
VIDAS_INICIO = 5
PONDERADOR_DIFICULTAD = 0.9
CANTIDAD_MONEDAS = 1

VELOCIDAD_AUTOS = 200
VELOCIDAD_TRONCOS = 75
VELOCIDAD_CAMINAR = 100
PIXELES_SALTO = LANE_WIDTH
JUMP_SPEED_BONUS = 2
SKULL_BONUS = 1.05

TIEMPO_AUTOS = 2
TIEMPO_TRONCOS = 2
TIEMPO_OBJETO = 5

CAR_SIZE = QSizeF(50, 50)
LOG_SIZE = QSizeF(100, 50)
ITEM_SIZE = QSizeF(50, 50)

FROG_SIZE = QSizeF(40, 40)
FROG_SKIN_0 = "Naranjo"

PATH_LOGO = os.path.join("sprites", "Logo.png")
PATH_GRASS = os.path.join("sprites", "Mapa", "areas", "pasto.png")
PATH_HIGHWAY = os.path.join("sprites", "Mapa", "areas", "carretera.png")
PATH_RIVER = os.path.join("sprites", "Mapa", "areas", "rio.png")
PATH_CAR_RIGHT = os.path.join("sprites", "Mapa", "autos", "rojo_right.png")
PATH_CAR_LEFT = os.path.join("sprites", "Mapa", "autos", "rojo_left.png")
PATH_LOG = os.path.join("sprites", "Mapa", "elementos", "tronco.png")

PATH_LIFE = os.path.join("sprites", "Objetos", "Corazon.png")
PATH_SKULL = os.path.join("sprites", "Objetos", "Calavera.png")
PATH_COIN = os.path.join("sprites", "Objetos", "Moneda.png")
PATH_CLOCK = os.path.join("sprites", "Objetos", "Reloj.png")

PATH_SCORES = "puntajes.txt"

PREFIX_FROG = os.path.join("sprites", "Personajes")
PREFIX_ITEM = os.path.join("sprites", "Objetos")

VIDAS_TRAMPA = 1
CHEAT_LIFE = [Qt.Key_V, Qt.Key_I, Qt.Key_D]
CHEAT_LEVEL = [Qt.Key_N, Qt.Key_I, Qt.Key_V]
