class PiezaSencilla:
    def __init__(self, center= [0, 0], angle=0, v1=-1, v2=-1):
        """Clase que define una pieza de domino mas sencilla, con menos cosas

        Args:
            ...
        """
        self.center = center
        self.angle = angle
        self.v1 = v1
        self.v2 = v2
          
    def esDoble(self):
        if self.v1 == self.v2:
            return True
        else:
            return False
        
    def esVertical(self):
        if abs(self.angle - 90) < 45:
            return True
        else:
            return False

    def esHorizontal(self):
        if abs(self.angle) < 45:
            return True
        else:
            return False

    def sumaValor(self):
        return self.v1 + self.v2
    

def convertir