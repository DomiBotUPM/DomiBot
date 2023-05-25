import os
import cv2

from vision.vision_interface import DominoVision
from vision.conversion_coordenadas import conversionCoordenadasJuego

import decision_jugada.domino_game as domigame
import decision_jugada.colocar_pieza as colopieza
from decision_jugada.logica import logica, logica_test
from decision_jugada.pieza_sencilla import PiezaSencilla, tablero2piezas

# esto son constantes que me he inventado
ORDEN_NORMA = 2
LONGITUD_PIEZA  = 80
ANCHURA_PIEZA   = 40 
UMBRAL_DIST     = LONGITUD_PIEZA * 1.5
ALTO_IMG        = 480
ANCHO_IMG       = 640
ALTO_MANO_ROBOT = 140 
LIMITE1 = 100
LIMITE2 = 540

domino_vision = DominoVision(visualize=False, verbose=False)

# Probar con imagenes

path_dir = os.path.abspath("vision/fotos_test/")

file_robot = "robotdoble.jpg"
file_tablero = "tablerounapieza.jpg"

filename_robot = os.path.join(path_dir, file_robot)
img_robot = cv2.imread(filename_robot)


filename_tablero = os.path.join(path_dir, file_tablero)
img_tablero = cv2.imread(filename_tablero)


size = img_robot.shape[0]*img_robot.shape[1]

# visión
detections_tablero = domino_vision.pieces_detection(img_tablero, size, size_mm=0)
recognitions_tablero = domino_vision.pieces_recognition(img_tablero, size, pieces=detections_tablero)

detections_robot = domino_vision.pieces_detection(img_robot, size, size_mm=0)
recognitions_robot = domino_vision.pieces_recognition(img_robot, size, pieces=detections_robot)


print("recognitions tablero")
for pieza in recognitions_tablero:
    print([pieza.dots, pieza.center, pieza.center_mm, pieza.angle])

print("recognitions robot")
for pieza in recognitions_robot:
    print([pieza.dots, pieza.center, pieza.center_mm, pieza.angle])

# # Ordena las piezas
# piezas_ordenadas = domino_vision.ordenar_piezas(domino_vision.pieces)

# print("piezas_ordenadas: ")
# for pieza in piezas_ordenadas:
#     print([pieza.dots, pieza.center, pieza.center_mm, pieza.angle])

valores_piezas_robot = []
valores_piezas_tablero = []

# valores reales
# for pieza in recognitions:
#     posicion_pieza = conversionCoordenadasJuego(pieza.center_mm[0], pieza.center_mm[1], pieza.angle)
#     posicion_pieza[0] /= 1000 # paso a m
#     posicion_pieza[1] /= 1000 # paso a m
#     if len(pieza.dots) == 2:
#         posicion_pieza.extend([pieza.dots[0], pieza.dots[1]])
#     else:
#         posicion_pieza.extend([-1, -1])
#     valores_piezas.append(posicion_pieza)

# en pixeles
for pieza in recognitions_robot:
    #posicion_pieza = conversionCoordenadasJuego(pieza.center[0], pieza.center[1], pieza.angle)
    posicion_pieza = [pieza.center[0], pieza.center[1], pieza.angle]
    # posicion_pieza[0] /= 1000 # paso a mm
    # posicion_pieza[1] /= 1000 # paso a mm
    if len(pieza.dots) == 2:
        posicion_pieza.extend([pieza.dots[0], pieza.dots[1]])
    else:
        posicion_pieza.extend([-1, -1])
    valores_piezas_robot.append(posicion_pieza)

for pieza in recognitions_tablero:
    #posicion_pieza = conversionCoordenadasJuego(pieza.center[0], pieza.center[1], pieza.angle)
    posicion_pieza = [pieza.center[0], pieza.center[1], pieza.angle]
    # posicion_pieza[0] /= 1000 # paso a m
    # posicion_pieza[1] /= 1000 # paso a m
    if len(pieza.dots) == 2:
        posicion_pieza.extend([pieza.dots[0], pieza.dots[1]])
    else:
        posicion_pieza.extend([-1, -1])
    valores_piezas_tablero.append(posicion_pieza)

piezas_sencillas_robot = tablero2piezas(valores_piezas_robot)
piezas_sencillas_tablero = tablero2piezas(valores_piezas_tablero)

# print("Piezas sencillas")
# for pieza in piezas_sencillas_robot:
#     print([[pieza.v1, pieza.v2], pieza.center, pieza.angle])

# Separa las piezas segun sean del robot o del tablero
# piezas_tablero, piezas_robot = domigame.clasificarPiezas(piezas_sencillas_robot, ALTO_IMG, ALTO_MANO_ROBOT)

print("piezas_tablero: ")
print([[pieza.v1, pieza.v2] for pieza in piezas_sencillas_tablero])
print("piezas_robot: ")
print([[pieza.v1, pieza.v2] for pieza in piezas_sencillas_robot])

jugada_logica =  logica_test(piezas_sencillas_tablero, piezas_sencillas_robot)
print(jugada_logica)

origen0, origen1, angulo_origen, destino0, destino1, angulo_destino = jugada_logica

#  = cv2.imread(filename_robot)
img_robot = cv2.circle(img_robot, (int(origen0),int(origen1)), radius=20, color=(0, 0, 255), thickness=3)
cv2.imshow("Movimiento origen", img_robot)

img_tablero = cv2.circle(img_tablero, (int(destino0),int(destino1)), radius=20, color=(255, 255, 0), thickness=3)
img_tablero = cv2.putText(img_tablero, str(round(angulo_destino,1)) + " deg", (int(destino0), int(destino1)-30), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1, cv2.LINE_AA)
cv2.imshow("Movimiento destino", img_tablero)

cv2.waitKey(0)