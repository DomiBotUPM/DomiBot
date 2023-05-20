# import sys
# sys.path.append("..\vision")

from .colocar_pieza import colocarPieza
from .domino_game import tableroVirtual, decidirMovimiento
from .pieza_sencilla import PiezaSencilla, tablero2piezas, robot2piezas

def logica(valores_tablero, valores_robot):
    ORDEN_NORMA = 2
    # LONGITUD_PIEZA  = 80 # en píxeles
    # ANCHURA_PIEZA   = 40 # en píxeles  
    LONGITUD_PIEZA  = 0.038 # en m
    ANCHURA_PIEZA   = 0.019 # en m
    UMBRAL_DIST     = LONGITUD_PIEZA * 1.5
    # limites para no colocar en los extremos
    # LIMITE1 = 100
    # LIMITE2 = 540
    LIMITE1 = 0.050
    LIMITE2 = 0.0314 - 0.050

    # interpretar los arrays que me pasan y convertirlos en piezas
    piezas_robot = robot2piezas(valores_robot)
    piezas_tablero = tablero2piezas(valores_tablero)

    # Crear tablero virtual (ordenar las piezas)
    tablero = tableroVirtual(piezas_tablero, UMBRAL_DIST, ORDEN_NORMA)

    # Decidir el movimiento
    movimiento = decidirMovimiento(tablero, piezas_robot)

    # Coordenadas del movimiento (origne, destino) -> coordenadas imagen
    origen, angulo_origen, destino, angulo_destino = colocarPieza(movimiento, LIMITE1, LIMITE2, LONGITUD_PIEZA, ANCHURA_PIEZA, tablero)

    return [origen[0], destino[0], destino[1], angulo_destino]


def logica_test(piezas_tablero, piezas_robot):
    ORDEN_NORMA = 2
    LONGITUD_PIEZA  = 80 # en píxeles
    ANCHURA_PIEZA   = 40 # en píxeles  
    # LONGITUD_PIEZA  = 0.038 # en m
    # ANCHURA_PIEZA   = 0.019 # en m
    UMBRAL_DIST     = LONGITUD_PIEZA * 1.5
    # limites para no colocar en los extremos
    LIMITE1 = 100
    LIMITE2 = 540
    # LIMITE1 = 0.050
    # LIMITE2 = 0.0314 - 0.050

    # Crear tablero virtual (ordenar las piezas)
    tablero = tableroVirtual(piezas_tablero, UMBRAL_DIST, ORDEN_NORMA)

    # Decidir el movimiento
    movimiento = decidirMovimiento(tablero, piezas_robot)

    # Coordenadas del movimiento (origne, destino) -> coordenadas imagen
    origen, angulo_origen, destino, angulo_destino = colocarPieza(movimiento, LIMITE1, LIMITE2, LONGITUD_PIEZA, ANCHURA_PIEZA, tablero)

    return [origen[0], origen[1], angulo_origen, destino[0], destino[1], angulo_destino]