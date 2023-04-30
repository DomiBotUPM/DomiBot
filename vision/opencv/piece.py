import numpy as np
from typing import List

class Piece:
    def __init__(self, mask: np.ndarray, contour: np.ndarray, center: tuple, angle: float, size: tuple, type: str = "") -> None:
        self.mask = mask
        self.contour = contour
        self.center = center
        self.angle = angle
        self.size = size
        self.type = type
        self.center_mm = 0.0
        self.size_mm = 0.0
        self.dots: List[int] = []
        
    def __dir__(self):
        print(f"Angulo: {self.angle}, size: {self.size}, type: {self.type}, center: {self.center}")