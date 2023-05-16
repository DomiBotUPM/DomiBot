import sys
sys.path.append("..\vision")

from .colocar_pieza import colocarPieza
from .domino_game import tableroVirtual, decidirMovimiento
from vision.opencv.piece import Piece

# LEER, IMPORTANTE
# No sé si funciona esto porque está hecho muy a huevo y no he depurado casi nada. Solo funciona, 
# si las piezas son horizontales y verticales, para lo cual hay que usar mi versión de la visión.
# Esta versión mía de la visión (v3) solo funciona con piezas ligermaente separadas. En caso de tener
# que robar, devuelve 0, 0, 0, 0...



def logica(piezas_tablero, piezas_robot):
    ORDEN_NORMA = 2
    LONGITUD_PIEZA  = max(piezas_tablero[0].size)
    ANCHURA_PIEZA   = min(piezas_tablero[0].size) 
    UMBRAL_DIST     = LONGITUD_PIEZA * 1.5
    # límites para no colocar en los extremos
    LIMITE1 = 100
    LIMITE2 = 540


    # Crear tablero virtual (ordenar las piezas)
    tablero = tableroVirtual(piezas_tablero, UMBRAL_DIST, ORDEN_NORMA)

    # Decidir el movimiento
    movimiento = decidirMovimiento(tablero, piezas_robot)

    # Coordenadas del movimiento (origne, destino) -> coordenadas imagen
    origen, angulo_origen, destino, angulo_destino = colocarPieza(movimiento, LIMITE1, LIMITE2, LONGITUD_PIEZA, ANCHURA_PIEZA, tablero)

    return [origen[0], origen[1], angulo_origen, destino[0], destino[1], angulo_destino]