# Que nombre mas malo de archivo

import os
from vision.vision_interface import DominoVision
import cv2 as cv
import sys
from vision.conversion_coordenadas import conversionCoordenadasJuego

# datos generales
width_game = 314
height_game = 236
# les he dado la vuelta respecto a lo que hizo JP 
area_game = width_game*height_game
domino_vision = DominoVision(visualize=False, verbose=False)

# captura
capture = cv.VideoCapture(0)
ret, frame = capture.read()

# datos de captura
# width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
# height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
width = 640
height = 480
size = width*height

detections = domino_vision.pieces_detection(frame, size, size_mm=area_game)
recognitions = domino_vision.pieces_recognition(frame, size, pieces=detections)

valores_piezas = []

for pieza in recognitions:
    posicion_pieza = conversionCoordenadasJuego(pieza.center_mm[0], pieza.center_mm[1], pieza.angle)
    posicion_pieza[0] /= 1000 # paso a mm
    posicion_pieza[1] /= 1000 # paso a mm
    valores_piezas.extend(posicion_pieza)
    if len(pieza.dots) == 2:
        valores_piezas.extend([pieza.dots[0], pieza.dots[1]])
    else:
        valores_piezas.extend([-1, -1])

print(valores_piezas)

