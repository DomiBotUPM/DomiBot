
import cv2 as cv
import numpy as np
from typing import List, Tuple
PIECE_WIDTH_MM = 19
PIECE_HEIGHT_MM = 38

def get_ratio_px2mm_from_piece(piece: dict) -> float:
    """Obtener el ratio de conversion de pixeles a milimetros, a partir de una pieza. 

    Args:
        piece (dict): Datos de la pieza. Sera necesario al menos el ancho en pixeles.

    Returns:
        float: Ratio de conversion
    """
    return PIECE_WIDTH_MM / piece['size_px'][0]

def piece_location(piece: dict, ratio_px2mm: float, verbose=False, img=None, visualize=False) -> Tuple[float, Tuple[float,float], float]:
    """Localizar la pieza con respecto a la imagen o captura realizada

    Args:
        piece (dict): Datos de pieza. Contendra al menos el centro y el tamano en pixeles, asi como el angulo de rotacion.
        ratio_px2mm (float): Ratio de conversion de pixeles a milimetros
        verbose (bool, optional): Mostrar mensajes de seguimiento. Defaults to False.
        img (Mat): Imagen para visualizar. Solo es necesario si visualize es True
        visualize (bool, optional): Visualizar imagen resultante. Defaults to False.

    Returns:
        Tuple[float, Tuple[float,float], float]: _description_
    """
    center = np.round(ratio_px2mm * piece['center'], 2)
    width = round(ratio_px2mm * piece['size_px'][0], 2)
    height = round(ratio_px2mm * piece['size_px'][1], 2)
    if visualize and img is not None:
        cx = round(piece['center'][0])
        cy = round(piece['center'][1])
        cv.rectangle(img, (cx-34, cy-6), (cx+34, cy+6), (255,255,255), thickness=-1)
        cv.putText(img, f"({round(center[0],1)}, {round(center[1],1)})", (cx-33, cy+3), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0), 1, cv.LINE_AA)
        cv.imshow("Localizacion de piezas", img)
    return center, (width,height), piece['angle']

def pieces_location(pieces: List[dict], verbose=False, img=None, visualize=False) -> List[Tuple[float, Tuple[float,float], float]]:
    """Localizar la pieza con respecto a la imagen o captura realizada

    Args:
        pieces (List[dict]): Piezas estructuradas como una lista de diccionarios. Sera necesario el centro y el tamano en pixeles, asi como el angulo.
        verbose (bool, optional): Mostrar mensajes de seguimiento. Defaults to False.
        img (Mat): Imagen para visualizar. Solo es necesario si visualize es True
        visualize (bool, optional): Visualizar imagen resultante. Defaults to False.

    Returns:
        List[Tuple[float, Tuple[float,float], float]]: Lista de localizaciones. Indica: centro en mm, (ancho,alto) en mm y angulo de rotacion en º.
    """
    if img is not None:
        img_i = img.copy()
    else:
        img_i = img
    ratio_px2mm = get_ratio_px2mm_from_piece(pieces[0])
    locations = []
    for piece in pieces:
        locations.append(piece_location(piece, ratio_px2mm, verbose, img_i, visualize))
    return locations
        