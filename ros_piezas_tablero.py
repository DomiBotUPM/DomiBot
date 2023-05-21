# ROS_PIEZAS_TABLERO
# Ejecutar para conocer las piezas que hay en el tablero de juego. Es necesario decir la posicion correctamente. 

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

# convierte datos de piezas en un array del tipo
# [[pieza1.x, pieza1.y, pieza1.angulo, pieza1.valor1, pieza1.valor2], [pieza2.x, pieza2.y, pieza2.angulo, pieza2.valor1, pieza2.valor2], ...]
# Si no detecta puntos (por error o porque esta dada la vuelta), los valores son -1 y -1
for pieza in recognitions:
    # primero, convertir las coordenadas a absolutas
    posicion_pieza = conversionCoordenadasJuego(pieza.center_mm[0], pieza.center_mm[1], pieza.angle)
    posicion_pieza[0] /= 1000 # paso mm a m
    posicion_pieza[1] /= 1000 # paso mm a m
    if len(pieza.dots) == 2:
        posicion_pieza.extend([pieza.dots[0], pieza.dots[1]])
    else:
        posicion_pieza.extend([-1, -1])
    valores_piezas.append(posicion_pieza)

print(valores_piezas)

