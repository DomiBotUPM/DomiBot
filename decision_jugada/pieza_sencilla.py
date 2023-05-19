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
        if abs(self.angle) < 45 or abs(self.angle - 180) < 45:
            return True
        else:
            return False

    def sumaValor(self):
        return self.v1 + self.v2
    

def tablero2piezas(valores_tablero):
    piezas = []
    for valores in valores_tablero:
        pieza = PiezaSencilla(x=valores[0], y=valores[1], angle=valores[2], v1=valores[3], v2=valores[4])
        piezas.append(pieza)
    return piezas

def robot2piezas(valores_robot):
    piezas = []
    for i in range(len(valores_robot)):
        if valores_robot[i][0]:
            pieza = PiezaSencilla(x=i, y=0, angle=0, v1=valores_robot[i][0], v2=valores_robot[i][1])
        piezas.append(pieza)
    return piezas


