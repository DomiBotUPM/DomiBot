# ROS_PIEZAS_ROBOT

import os
from vision.vision_interface import DominoVision
import cv2 as cv
import sys
from vision.conversion_coordenadas import conversionCoordenadasJuego

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

detections = domino_vision.pieces_detection(frame, size)
recognitions = domino_vision.pieces_recognition(frame, size, pieces=detections)
recognitions = domino_vision.ordenar_piezas(recognitions)

valores_piezas = []

for pieza in recognitions:
    if len(pieza.dots) == 2:
        valores_piezas.extend([pieza.dots[0], pieza.dots[1]])
    else:
        valores_piezas.extend([-1, -1])

print(valores_piezas)