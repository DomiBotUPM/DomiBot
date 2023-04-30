import math
import numpy as np
from operator import itemgetter


def distanciaPiezas(pieza1, pieza2, orden):
    c1 = np.array(pieza1['center'])
    c2 = np.array(pieza2['center'])

    return np.linalg.norm(c1 - c2, ord = orden)

def masCercanos(pieza_elegida, piezas, orden):
    distancias = []

    for pieza in piezas:
        distancias.append(distanciaPiezas(pieza_elegida, pieza, orden))

    indices_orden = sorted(range(len(distancias)), key=lambda k: distancias[k]) # stack overflow

    return indices_orden, distancias


def tableroVirtual(piezas, umbral_dist, orden):
    if len(piezas) == 1:
        return piezas
    elif len(piezas) == 2:
        if distanciaPiezas(piezas[0], piezas[1], orden) <= umbral_dist:
            return piezas
        else:
            return [piezas[0]]
        
    tablero = [piezas[0]]
    piezas_restantes = piezas[1:]

    print([pieza['type'] for pieza in tablero])

    while piezas_restantes:
        ind, dist = masCercanos(tablero[-1], piezas_restantes, orden)
        if dist[ind[0]] <= umbral_dist:
            tablero.append(piezas_restantes[ind[0]])
            piezas_restantes.pop(ind[0])
            print([pieza['type'] for pieza in tablero])
        else:
            break

    if piezas_restantes:
        tablero.reverse()
    else:
        return tablero
    print([pieza['type'] for pieza in tablero])

    while piezas_restantes:
        ind, dist = masCercanos(tablero[-1], piezas_restantes, orden)
        if dist[ind[0]] <= umbral_dist:
            tablero.append(piezas_restantes[ind[0]])
            piezas_restantes.pop(ind[0])
            print([pieza['type'] for pieza in tablero])
        else:
            break
    
    return tablero


    
    


    



