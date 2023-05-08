import os
import decision_jugada.domino_game as domigame
from vision.vision_interface import DominoVision
import cv2

ORDEN_NORMA = 2
LONGITUD_PIEZA  = 80
ANCHURA_PIEZA   = 40
UMBRAL_DIST     = LONGITUD_PIEZA * 1.5
ALTO_IMG        = 480
ANCHO_IMG       = 640
ALTO_MANO_ROBOT = 140


domino_vision = DominoVision(visualize=True, verbose=False)

# Probar con imagenes

path_dir = os.path.abspath("vision/fotos_ur3/")

# file = "PIEZAS_TEST.jpg"
# file = "CADENA3.jpg"  
file = "20230412_194341.jpg"
filename = os.path.join(path_dir, file)
# img = cv2.imread(filename)
# size = img.shape[0]*img.shape[1]

domino_vision.test_with_image(filename)

print([[pieza.dots, pieza.type] for pieza in domino_vision.pieces])

# print([[pieza.esVertical(), pieza.type, pieza.getRealValue()] for pieza in domino_vision.pieces])
# print([domino_vision.pieces[0].contour, pieza.type], domino_vision.pieces[0].type)


# # Separa las piezas según sean del robot o del tablero
# piezas_tablero, piezas_robot = domigame.clasificarPiezas(domino_vision.pieces, ALTO_IMG, ALTO_MANO_ROBOT)

# print("piezas_tablero: ")
# print([pieza.type for pieza in piezas_tablero])
# print("piezas_robot: ")
# print([pieza.type for pieza in piezas_robot])

# # Crea tablero virtual (ordena las piezas)
# tablero = domigame.tableroVirtual(piezas_tablero, UMBRAL_DIST, ORDEN_NORMA)

# print("tablero: ")
# print([pieza.type for pieza in tablero])

# # ¿qué pieza se puede colocar?
# movimiento = domigame.decidirMovimiento(tablero, piezas_robot)

# print("movimiento: ")
# print(movimiento["movimiento"])
# if "pieza_tablero" in movimiento:
#     print(movimiento["pieza_tablero"].type)
#     print(movimiento["pieza_robot"].type)