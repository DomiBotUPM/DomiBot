import os
import decision_jugada.domino_game as domigame
import decision_jugada.colocar_pieza as colopieza
from decision_jugada.logica import logica
from vision.vision_interface import DominoVision
import cv2
from vision.conversion_coordenadas import conversionCoordenadasJuego

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

domino_vision = DominoVision(visualize=True, verbose=False)

# Probar con imagenes

path_dir = os.path.abspath("vision/fotos_ur3/")


# file = "AAAAA.jpg"
# file = "PIEZAS_TEST2.jpg"
file = "CADENA4.jpg"
filename = os.path.join(path_dir, file)

img = cv2.imread(filename)
size = img.shape[0]*img.shape[1]

detections = domino_vision.pieces_detection(img, size, size_mm=0)
recognitions = domino_vision.pieces_recognition(img, size, pieces=detections)
recognitions = domino_vision.ordenar_piezas(recognitions)

print("recognitions")
for pieza in recognitions:
    print([pieza.dots, pieza.center, pieza.center_mm, pieza.angle])

# conversión de coordenadas
# x_px = recognitions[0].center_mm[0]
# y_px = recognitions[0].center_mm[1]
# theta_px = recognitions[0].angle

# coord = conversionCoordenadasJuego(x_px, y_px, theta_px)
# print(coord)

# # Ordena las piezas
# piezas_ordenadas = domino_vision.ordenar_piezas(domino_vision.pieces)

# print("piezas_ordenadas: ")
# for pieza in piezas_ordenadas:
#     print([pieza.dots, pieza.center, pieza.center_mm, pieza.angle])

# Separa las piezas segun sean del robot o del tablero
piezas_tablero, piezas_robot = domigame.clasificarPiezas(recognitions, ALTO_IMG, ALTO_MANO_ROBOT)

print("piezas_tablero: ")
print([pieza.type for pieza in piezas_tablero])
print("piezas_robot: ")
print([pieza.type for pieza in piezas_robot])

jugada_logica =  logica(piezas_tablero, piezas_robot)
print(jugada_logica)
# print(origen0, origen1, angulo_origen, destino0, destino1, angulo_destino)

# origen0, origen1, angulo_origen, destino0, destino1, angulo_destino = jugada_logica

# img = cv2.imread(filename)
# img = cv2.circle(img, (int(origen0),int(origen1)), radius=20, color=(0, 0, 255), thickness=3)
# img = cv2.circle(img, (int(destino0),int(destino1)), radius=20, color=(255, 255, 0), thickness=3)
# cv2.imshow("Imagen real", img)


cv2.waitKey(0)