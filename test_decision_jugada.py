from vision.opencv.pieces_recognition_v1 import pieces_recognition
import decision_jugada.domino_game as dg
import os
import cv2
import math

LONGITUD_PIEZA  = 80
ANCHURA_PIEZA   = 40
ORDEN_NORMA     = 2
UMBRAL_DIST     = LONGITUD_PIEZA * 1.5


#copypaste de la parte de Jean Paul
path_dir = "vision/fotos_ur3/"
filename = os.path.join(path_dir, "CADENA2.jpg")
img = cv2.imread(filename)

piezas = pieces_recognition(img, size=img.shape[0]*img.shape[1], preprocess=True, verbose=False, visualize=True)

print([pieza['type'] for pieza in piezas])

tablero = dg.tableroVirtual(piezas, UMBRAL_DIST, ORDEN_NORMA)

print([pieza['type'] for pieza in tablero])

cv2.waitKey(0)
cv2.destroyAllWindows()