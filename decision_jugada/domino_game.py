import sys
sys.path.append("..\vision")

import numpy as np
# from operator import itemgetter
from vision.opencv.piece import Piece

def distanciaPiezas(pieza1: Piece, pieza2: Piece, orden):
    c1 = np.array(pieza1.center)
    c2 = np.array(pieza2.center)

    return np.linalg.norm(c1 - c2, ord = orden)

def masCercanos(pieza_elegida: Piece, piezas: Piece, orden):
    distancias = []

    for pieza in piezas:
        distancias.append(distanciaPiezas(pieza_elegida, pieza, orden))

    indices_orden = sorted(range(len(distancias)), key=lambda k: distancias[k]) # stack overflow

    return indices_orden, distancias

def numeroComun(pieza1: Piece, pieza2: Piece):
    if pieza1.type[0] == pieza2.type[0]:
        return pieza1.type[0]
    elif pieza1.type[0] == pieza2.type[2]:
        return pieza1.type[0]
    elif pieza1.type[2] == pieza2.type[0]:
        return pieza1.type[2]
    elif pieza1.type[2] == pieza2.type[2]:
        return pieza1.type[2]
    else: 
        return -1
    
def numeroDiferenteExtremo(pieza_extremo: Piece, pieza_interior: Piece):
    if pieza_extremo.type[0] == pieza_interior.type[0]:
        return pieza_extremo.type[2]
    elif pieza_extremo.type[0] == pieza_interior.type[2]:
        return pieza_extremo.type[2]
    elif pieza_extremo.type[2] == pieza_interior.type[0]:
        return pieza_extremo.type[0]
    elif pieza_extremo.type[2] == pieza_interior.type[2]:
        return pieza_extremo.type[0]
    else: 
        return -1

def extremosTablero(tablero: Piece):
    if len(tablero) == 0:
        return [0, 1, 2, 3, 4, 5, 6]
    elif len(tablero) == 1: # en teoría siempre debería ser doble pero bueeeno
        if tablero[0].esDoble():
            return [tablero[0].type[0]]
        else:
            return [tablero[0].type[2]]
        
    nc1 = numeroDiferenteExtremo(tablero[0], tablero[1])
    nc2 = numeroDiferenteExtremo(tablero[-1], tablero[-2])
    return [nc1, nc2]


def jugadasDisponibles(tablero: Piece, piezas_robot: Piece):
    extremos = extremosTablero(tablero)

    posibles_jugadas_1 = []
    posibles_jugadas_2 = []

    for pieza in piezas_robot:
        if pieza.type[0] == extremos[0] or pieza.type[2] == extremos[0]:
            posibles_jugadas_1.append(pieza)
        if pieza.type[0] == extremos[1] or pieza.type[2] == extremos[1]:
            posibles_jugadas_2.append(pieza)
    
    return posibles_jugadas_1, posibles_jugadas_2


# #######################################
# ######## FUNCIONES IMPORTANTES ########
# #######################################


def clasificarPiezas(piezas: Piece, alto_imagen, alto_zona_robot):
    piezas_tablero= [] 
    piezas_robot = []

    for pieza in piezas:
        if alto_imagen - pieza.center[1] - 1 < alto_zona_robot:
            piezas_robot.append(pieza)
        else:
            piezas_tablero.append(pieza)

    return piezas_tablero, piezas_robot


def tableroVirtual(piezas: Piece, umbral_dist, orden):
    if len(piezas) == 1:
        return piezas
    elif len(piezas) == 2:
        if distanciaPiezas(piezas[0], piezas[1], orden) <= umbral_dist:
            return piezas
        else:
            return [piezas[0]]
        
    tablero = [piezas[0]]
    piezas_restantes = piezas[1:]

    # print([pieza.type for pieza in tablero])

    while piezas_restantes:
        ind, dist = masCercanos(tablero[-1], piezas_restantes, orden)
        if dist[ind[0]] <= umbral_dist:
            tablero.append(piezas_restantes[ind[0]])
            piezas_restantes.pop(ind[0])
            # print([pieza.type for pieza in tablero])
        else:
            break

    if piezas_restantes:
        tablero.reverse()
    else:
        return tablero
    # print([pieza.type for pieza in tablero])

    while piezas_restantes:
        ind, dist = masCercanos(tablero[-1], piezas_restantes, orden)
        if dist[ind[0]] <= umbral_dist:
            tablero.append(piezas_restantes[ind[0]])
            piezas_restantes.pop(ind[0])
            # print([pieza.type for pieza in tablero])
        else:
            break
    
    return tablero


def decidirMovimiento(tablero: Piece, piezas_robot: Piece): # aquí viene toda la IA :)
    posibles_jugadas1, posibles_jugadas2 = jugadasDisponibles(tablero, piezas_robot)

    if len(posibles_jugadas1): # hay jugadas posibles para la primera ficha del tablero
        #para elegir ficha de mayor valor
        suma_valores1 = [pieza.sumaValor() for pieza in posibles_jugadas1]
        ind_orden1 = sorted(range(len(suma_valores1)), key=lambda k: suma_valores1[k]) # stack overflow

        if len(posibles_jugadas2): # hay jugadas posibles para ambos extremos del tablero
            #para elegir ficha de mayor valor
            suma_valores2 = [pieza.sumaValor() for pieza in posibles_jugadas2]
            ind_orden2 = sorted(range(len(suma_valores2)), key=lambda k: suma_valores2[k]) # stack overflow

            if suma_valores1[ind_orden1[-1]] >= suma_valores2[ind_orden2[-1]]:
                return {'movimiento': 'jugada', 'pieza_tablero': tablero[0], 'pieza_robot': posibles_jugadas1[ind_orden1[-1]]}
            else:
                return {'movimiento': 'jugada', 'pieza_tablero': tablero[-1], 'pieza_robot': posibles_jugadas2[ind_orden2[-1]]}
        else:
            return {'movimiento': 'jugada', 'pieza_tablero': tablero[0], 'pieza_robot': posibles_jugadas1[ind_orden1[-1]]}
        
    elif len(posibles_jugadas2): # hay jugadas posibles para la última ficha del tablero pero no para la primera
        #para elegir ficha de mayor valor
        suma_valores2 = [pieza.sumaValor() for pieza in posibles_jugadas2]
        ind_orden2 = sorted(range(len(suma_valores2)), key=lambda k: suma_valores2[k]) # stack overflow
        return {'movimiento': 'jugada', 'pieza_tablero': tablero[-1], 'pieza_robot': posibles_jugadas2[ind_orden2[-1]]}
    
    else:
        return {'movimiento': 'robar'}
