import sys
sys.path.append("..\vision")

import numpy as np
from vision.opencv.piece import Piece
from .domino_game import numeroComun

def piezasVerticalSeguidas(tablero: Piece, direccion, ancho_pieza):
    np = 0
    if direccion == 'arriba':
        tablero.reverse()
    for pieza in tablero:
        if abs(tablero[0].center[0] - pieza.center[0]) < ancho_pieza:
            if pieza.esDoble():
                continue
            else:
                np += 1
        else:
            return np
    return np

def proximaDireccionHorizontal(tablero: Piece, direccion):
    if len(tablero) == 1:
        return 'derecha'
    elif direccion == 'abajo':
        if tablero[0].center[0] < tablero[1].center[0]:
            return 'izquierda'
        else:
            return 'derecha'
    else:
        if tablero[-1].center[0] < tablero[-2].center[0]:
            return 'izquierda'
        else:
            return 'derecha'

# #######################################
# ######## FUNCIONES IMPORTANTES ########
# #######################################

def colocarPieza(movimiento, limite1, limite2, longitud_pieza, ancho_pieza, tablero):
    # establecer las coordenadas de la pieza que coges y dónde se coloca
    ratio_dist = 1.2

    if movimiento["movimiento"] == 'robar':
        print('Hey, no deberías estar aquí!')
        return 0, 0, 0, 0
    
    pieza_robot = movimiento["pieza_robot"]
    pieza_tablero = movimiento["pieza_tablero"]
    proxima_direccion_horizontal = proximaDireccionHorizontal(tablero, movimiento["direccion"])

    origen = pieza_robot.center

    # ------------- PIEZA ROBOT DOBLE ----------------
    if pieza_robot.esDoble():
        angulo_origen = pieza_robot.angle
        # HORIZONTAL + A LA IZQUIERDA
        if abs(pieza_tablero.angle) < 15 and proxima_direccion_horizontal == 'izquierda':
            destino = [pieza_tablero.center[0] - longitud_pieza, pieza_tablero.center[1]]
            angulo_destino = 90
        # HORIZONTAL + A LA DERECHA
        elif abs(pieza_tablero.angle) < 15 and proxima_direccion_horizontal == 'derecha':
            destino = [pieza_tablero.center[0] + longitud_pieza, pieza_tablero.center[1]]
            angulo_destino = 90 
        # VERTICAL + ABAJO
        elif movimiento["direccion"] == 'abajo':
            destino = [pieza_tablero.center[0], pieza_tablero.center[1] + longitud_pieza]
            angulo_destino = 0 
        # VERTICAL + ARRIBA
        else:
            destino = [pieza_tablero.center[0], pieza_tablero.center[1] - longitud_pieza]
            angulo_destino = 0 

    # ------------- PIEZA TABLERO DOBLE ----------------
    elif pieza_tablero.esDoble(): # más complicado :(
        numero_comun = numeroComun(pieza_robot, pieza_tablero)
        # pieza origen
        if pieza_robot.dots[0] == numero_comun:
            angulo_origen = pieza_robot.angle
        else:
            angulo_origen = pieza_robot.angle + 180
            
        # HORIZONTAL + ABAJO
        if abs(pieza_tablero.angle) < 15 and movimiento["direccion"] == 'abajo':
            destino = [pieza_tablero.center[0], pieza_tablero.center[1] + longitud_pieza]
            angulo_destino = 90
            angulo_origen += 0
        # HORIZONTAL + ARRIBA
        elif abs(pieza_tablero.angle) < 15 and movimiento["direccion"] == 'arriba':
            destino = [pieza_tablero.center[0] + longitud_pieza, pieza_tablero.center[1]]
            angulo_destino = 90
            angulo_origen += 180
        # VERTICAL + IZQUIERDA
        elif proxima_direccion_horizontal == 'izquierda':
            # poner a continuación
            if pieza_tablero.center[0] - longitud_pieza > limite1:
                destino = [pieza_tablero.center[0] - longitud_pieza, pieza_tablero.center[1]]
                angulo_destino = 0
                angulo_origen += 180
            # poner abajo 
            elif movimiento["direccion"] == 'abajo': # lío de hacerlo del revés
                destino = [pieza_tablero.center[0], pieza_tablero.center[1] + longitud_pieza*ratio_dist]
                angulo_destino = 90
                angulo_origen += 0
            # poner arriba
            else:
                destino = [pieza_tablero.center[0], pieza_tablero.center[1] - longitud_pieza*ratio_dist]
                angulo_destino = 90
                angulo_origen += 180
        # VERTICAL + DERECHA
        elif proxima_direccion_horizontal == 'derecha':
            # poner a continuación
            if pieza_tablero.center[0] + longitud_pieza < limite2:
                destino = [pieza_tablero.center[0] + longitud_pieza, pieza_tablero.center[1]]
                angulo_destino = 0
                angulo_origen += 0
            # poner abajo 
            elif movimiento["direccion"] == 'abajo': # lío de hacerlo del revés
                destino = [pieza_tablero.center[0], pieza_tablero.center[1] + longitud_pieza*ratio_dist]
                angulo_destino = 90
                angulo_origen += 0
            # poner arriba
            else:
                destino = [pieza_tablero.center[0], pieza_tablero.center[1] - longitud_pieza*ratio_dist]
                angulo_destino = 90
                angulo_origen += 180
        
    # ------------- NO DOBLES ----------------
    else:
        numero_comun = numeroComun(pieza_robot, pieza_tablero)

        # pieza origen
        if pieza_robot.dots[0] == numero_comun:
            angulo_origen = pieza_robot.angle
        else:
            angulo_origen = pieza_robot.angle + 180


        # HORIZONTAL + A LA IZQUIERDA -> ¿se podría mirar simplemente con el 'arriba' o 'abajo'? -> NO
        if abs(pieza_tablero.angle) < 15 and proxima_direccion_horizontal == 'izquierda':
            # poner a continuación
            if pieza_tablero.center[0] - longitud_pieza*ratio_dist > limite1:
                destino = [pieza_tablero.center[0] - longitud_pieza*ratio_dist, pieza_tablero.center[1]]
                angulo_destino = 0
                angulo_origen += 180
            # poner abajo 
            elif movimiento["direccion"] == 'abajo': # lío de hacerlo del revés
                destino = [pieza_tablero.center[0] - ancho_pieza/2, pieza_tablero.center[1] + longitud_pieza]
                angulo_destino = 90
                angulo_origen += 0
            # poner arriba
            else:
                destino = [pieza_tablero.center[0] - ancho_pieza/2, pieza_tablero.center[1] - longitud_pieza]
                angulo_destino = 90
                angulo_origen += 180
        # HORIZONTAL + A LA DERECHA
        elif abs(pieza_tablero.angle) < 15 and proxima_direccion_horizontal == 'derecha':
            # poner a continuación
            if pieza_tablero.center[0] + longitud_pieza*ratio_dist < limite2:
                destino = [pieza_tablero.center[0] + longitud_pieza*ratio_dist, pieza_tablero.center[1]]
                angulo_destino = 0
                angulo_origen += 0
            # poner abajo 
            elif movimiento["direccion"] == 'abajo': # lío de hacerlo del revés
                destino = [pieza_tablero.center[0] + ancho_pieza/2, pieza_tablero.center[1] + longitud_pieza]
                angulo_destino = 90
                angulo_origen += 0
            # poner arriba
            else:
                destino = [pieza_tablero.center[0] + ancho_pieza/2, pieza_tablero.center[1] - longitud_pieza]
                angulo_destino = 90
                angulo_origen += 180 
        # VERTICAL + ABAJO
        elif movimiento["direccion"] == 'abajo':
            # poner a la izquierda o derecha
            if piezasVerticalSeguidas(tablero, 'abajo', ancho_pieza) >= 3:
                # poner a la derecha (estás en izquierda)
                if abs(pieza_tablero.center[0] - limite1) < abs(pieza_tablero.center[0] - limite2):
                    destino = [pieza_tablero.center[0] + longitud_pieza, pieza_tablero.center[1] + ancho_pieza/2]
                    angulo_destino = 0
                    angulo_origen += 0
                # poner a la izquierda (estás en izquierda)
                else:
                    destino = [pieza_tablero.center[0] - longitud_pieza, pieza_tablero.center[1] + ancho_pieza/2]
                    angulo_destino = 0
                    angulo_origen += 180
            # poner abajo
            else:
                destino = [pieza_tablero.center[0], pieza_tablero.center[1] + longitud_pieza*ratio_dist]
                angulo_destino = 90
                angulo_origen += 0 
        # VERTICAL + ARRIBA
        else:
            # poner a la izquierda o derecha
            if piezasVerticalSeguidas(tablero, 'arriba', ancho_pieza) >= 3:
                # poner a la derecha (estás en izquierda)
                if abs(pieza_tablero.center[0] - limite1) < abs(pieza_tablero.center[0] - limite2):
                    destino = [pieza_tablero.center[0] + longitud_pieza, pieza_tablero.center[1] - ancho_pieza/2]
                    angulo_destino = 0
                    angulo_origen += 0
                # poner a la izquierda (estás en izquierda)
                else:
                    destino = [pieza_tablero.center[0] - longitud_pieza, pieza_tablero.center[1] - ancho_pieza/2]
                    angulo_destino = 0
                    angulo_origen += 180
            # poner arriba
            else:
                destino = [pieza_tablero.center[0], pieza_tablero.center[1] - longitud_pieza*ratio_dist]
                angulo_destino = 90
                angulo_origen += 180 

    angulo_origen = angulo_origen % 360

    return origen, angulo_origen, destino, angulo_destino

