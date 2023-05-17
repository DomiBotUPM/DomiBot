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
width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
size = width*height

detections = domino_vision.pieces_detection(frame, size, size_mm=area_game)
recognitions = domino_vision.pieces_recognition(frame, size, pieces=detections)
recognitions = domino_vision.ordenar_piezas(recognitions)

valores_piezas = []

for pieza in recognitions:
    posicion_pieza = conversionCoordenadasJuego(pieza.center[0], pieza.center[1], pieza.angle)
    valores_piezas.extend(posicion_pieza)


