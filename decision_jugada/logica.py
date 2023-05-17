# import sys
# sys.path.append("..\vision")

from .colocar_pieza import colocarPieza
from .domino_game import tableroVirtual, decidirMovimiento
from .pieza_sencilla import PiezaSencilla

# LEER, IMPORTANTE
# No se si funciona esto porque esta hecho muy a huevo y no he depurado casi nada. Solo funciona, 
# si las piezas son horizontales y verticales, para lo cual hay que usar mi version de la vision.
# Esta version mia de la vision (v3) solo funciona con piezas ligeramente separadas. En caso de tener
# que robar, devuelve 0, 0, 0, 0...



def logica(piezas_tablero, piezas_robot):
    ORDEN_NORMA = 2
    LONGITUD_PIEZA  = 80 # en píxeles
    ANCHURA_PIEZA   = 40 # en píxeles  
    # LONGITUD_PIEZA  = 38 # en mm
    # ANCHURA_PIEZA   = 19 # en mm
    UMBRAL_DIST     = LONGITUD_PIEZA * 1.5
    # limites para no colocar en los extremos
    LIMITE1 = 100
    LIMITE2 = 540
    # LIMITE1 = 50
    # LIMITE2 = 314 - 50

    # Crear tablero virtual (ordenar las piezas)
    tablero = tableroVirtual(piezas_tablero, UMBRAL_DIST, ORDEN_NORMA)

    # Decidir el movimiento
    movimiento = decidirMovimiento(tablero, piezas_robot)

    # Coordenadas del movimiento (origne, destino) -> coordenadas imagen
    origen, angulo_origen, destino, angulo_destino = colocarPieza(movimiento, LIMITE1, LIMITE2, LONGITUD_PIEZA, ANCHURA_PIEZA, tablero)

    return [origen[0], origen[1], angulo_origen, destino[0], destino[1], angulo_destino]

def logicaPosicionesFijas(piezas_tablero, piezas_robot):
    ORDEN_NORMA = 2
    # LONGITUD_PIEZA  = 80 # en píxeles
    # ANCHURA_PIEZA   = 40 # en píxeles  
    LONGITUD_PIEZA  = 38 # en mmS
    ANCHURA_PIEZA   = 19 # en mm
    UMBRAL_DIST     = LONGITUD_PIEZA * 1.5
    # limites para no colocar en los extremos
    LIMITE1 = 50
    LIMITE2 = 314 - 50


    # Crear tablero virtual (ordenar las piezas)
    tablero = tableroVirtual(piezas_tablero, UMBRAL_DIST, ORDEN_NORMA)

    # Decidir el movimiento
    movimiento = decidirMovimiento(tablero, piezas_robot)

    # Coordenadas del movimiento (origne, destino) -> coordenadas imagen
    origen, angulo_origen, destino, angulo_destino = colocarPieza(movimiento, LIMITE1, LIMITE2, LONGITUD_PIEZA, ANCHURA_PIEZA, tablero)

    return [origen[0], origen[1], angulo_origen, destino[0], destino[1], angulo_destino]