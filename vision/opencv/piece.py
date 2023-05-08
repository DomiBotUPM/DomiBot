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

        self.real_v = 0.0
        
    def __dir__(self):
        print(f"Angulo: {self.angle}, size: {self.size}, type: {self.type}, center: {self.center}")

    def esDoble(self):
        if self.type[0] == self.type[2]:
            return True
        else:
            return False
        
    # def esVertical(self): # vertical u horizontal
    #     # h = max(self.contour[0,:]) - min(self.contour[0,:])
    #     # v = max(self.contour[1,:]) - min(self.contour[1,:])
    #     return (self.size[1] > self.size[0]) ^ (self.angle > 45)
    
    # def getRealValue(self):
    #     if self.size[1] > self.size[0]:
    #         if self.angle > 45:
    #             # horizontal
    #             return self.dots[0]
    #         else:
    #             # vertical
    #             return self.dots[1]
    #     else:
    #         if self.angle > 45:
    #             # vertical
    #             return self.dots[0]
    #         else:
    #             # horizontal
    #             return self.dots[1]

    def sumaValor(self):
        return int(self.type[0]) + int(self.type[2])
    
    
    



