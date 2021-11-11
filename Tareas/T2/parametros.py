import os
from PyQt5.QtCore import QSize

MIN_CARACTERES = 1
MAX_CARACTERES = 12

GAME_AREA_SIZE = QSize(800, 13 * 38)
FRAME_RATE = 60

LANE_NUM = 13  # 3*3 para los rios y carreteras, 2 para el inicio y fin, y 2 para las transiciones
LANE_LENGTH = GAME_AREA_SIZE.width()
LANE_WIDTH = GAME_AREA_SIZE.height() / LANE_NUM

DURACION_RONDA_INICIAL = 100
VIDAS_INICIO = 5

VELOCIDAD_AUTOS = 10
VELOCIDAD_TRONCOS = 10

PATH_LOGO = os.path.join("sprites", "Logo.png")
PATH_GRASS = os.path.join("sprites", "Mapa", "areas", "pasto.png")
PATH_HIGHWAY = os.path.join("sprites", "Mapa", "areas", "carretera.png")
PATH_RIVER = os.path.join("sprites", "Mapa", "areas", "rio.png")
