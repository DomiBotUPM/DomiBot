import numpy as np
from typing import List

class Piece:
    def __init__(self, mask: np.ndarray, contour: np.ndarray, center: tuple, angle: float, size: tuple, type: str = "") -> None:
        """Clase que define una pieza de dominó

        Args:
            mask (np.ndarray): Máscara que contiene. Puede utilizarse para identificación
            contour (np.ndarray): Contorno de la ficha
            center (tuple): Centro de la pieza
            angle (float): Ángulo de rotación
            size (tuple): Tamaño
            type (str, optional): Tipo de pieza. Defaults to "" (cuando aún no se ha identificado la pieza).
        """
        self.mask = mask
        self.contour = contour
        self.center = center
        self.angle = angle
        self.size = size
        # Medidas en milímetros
        self.center_mm = 0.0
        self.size_mm = 0.0
        # Identificación
        self.type = type
        self.dots: List[int] = []
        
    def get_area(self, area_px=True) -> float:
        """Obtener el área de la pieza, ya sea en píxeles o en milímetros

        Args:
            area_px (bool, optional): True: área en píxeles. False: área en milímetros. Defaults to True.

        Returns:
            float: Área de la pieza
        """
        if area_px:
            return self.size[0]*self.size[1]
        else:
            return self.size_mm[0]*self.size_mm[1]
        
    def __eq__(self, piece: 'Piece') -> bool:
        """Comparación con otra pieza. Para que sea la misma deben tener una rotación y un centro similar, además de ser del mismo tipo.

        Args:
            piece (Piece): _description_

        Returns:
            bool: True: las piezas son iguales. False: las piezas son distintas
        """

        cond_center_x = (self.center[0] < 1.1*piece.center[0]) and (self.center[0] > 0.9*piece.center[0])
        cond_center_y = (self.center[1] < 1.1*piece.center[1]) and (self.center[1] > 0.9*piece.center[0])
        cond_ang = (self.angle < 1.1* piece.angle) and (self.angle > 0.9*piece.angle)
        cond_type = self.type == piece.type
        if cond_center_x and cond_center_y and cond_ang and cond_type:
            return True
        else:
            return False
        
    def __ne__(self, piece: 'Piece') -> bool:
        return not self.__eq__(piece)
        
    def __str__(self):
        return f"Pice - angle: {round(self.angle, 2)}, size: {np.round(self.size, 1)}, type: {self.type}, center: {np.round(self.center,1)}"