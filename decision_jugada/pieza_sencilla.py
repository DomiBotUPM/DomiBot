class PiezaSencilla:
    def __init__(self, x = 0, y = 0, angle=0, v1=-1, v2=-1):
        """Clase que define una pieza de domino mas sencilla, con menos cosas

        Args:
            ...
        """
        self.center = [x, y]
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
    

def convertirArray3(array):
    piezas = []
    for i in range(int(len(array)/3)):
        piezas.append(PiezaSencilla(array[3*i + 0], array[3*i + 1], array[3*i + 2]))
    return piezas

def convertirArray5(array):
    piezas = []
    for i in range(int(len(array)/5)):
        piezas.append(PiezaSencilla(array[5*i + 0], array[5*i + 1], array[5*i + 2], array[5*i + 3], array[5*i + 4]))
    return piezas
