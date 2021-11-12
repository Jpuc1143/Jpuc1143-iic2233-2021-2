import os
from PyQt5.QtCore import QSize, QSizeF

MIN_CARACTERES = 1
MAX_CARACTERES = 12

GAME_AREA_SIZE = QSize(800, 13 * 38)
FRAME_RATE = 20

DIR_DOWN = 0
DIR_RIGHT = 1
DIR_UP = 2
DIR_LEFT = 3

LANE_NUM = 13  # 3*3 para los rios y carreteras, 2 para el inicio y fin, y 2 para las transiciones
LANE_LENGTH = GAME_AREA_SIZE.width()
LANE_WIDTH = GAME_AREA_SIZE.height() / LANE_NUM

DURACION_RONDA_INICIAL = 100
VIDAS_INICIO = 5

VELOCIDAD_AUTOS = 200
VELOCIDAD_TRONCOS = 50

TIEMPOS_AUTOS = 5
TIEMPOS_TRONCOS = 5

CAR_SIZE = QSizeF(50, 50)
LOG_SIZE = QSizeF(100, 50)

PATH_LOGO = os.path.join("sprites", "Logo.png")
PATH_GRASS = os.path.join("sprites", "Mapa", "areas", "pasto.png")
PATH_HIGHWAY = os.path.join("sprites", "Mapa", "areas", "carretera.png")
PATH_RIVER = os.path.join("sprites", "Mapa", "areas", "rio.png")
PATH_CAR_RIGHT = os.path.join("sprites", "Mapa", "autos", "rojo_right.png")
PATH_CAR_LEFT = os.path.join("sprites", "Mapa", "autos", "rojo_left.png")
PATH_LOG = os.path.join("sprites", "Mapa", "elementos", "tronco.png")
