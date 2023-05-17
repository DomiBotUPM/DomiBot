def conversionCoordenadasJuego(x_px, y_px, theta_px, x_robot = 270, y_robot = 196, alto_juego = 236, ancho_juego = 314, sep_camara = 60):
    x = alto_juego - y_px    # x del robot 
    y = ancho_juego - x_px    # y del robot 
    x = x - alto_juego / 2 + sep_camara + x_robot
    y = y - alto_juego / 2 + y_robot
    if abs(theta_px) < 30:
        theta = 90
    else:
        theta = 0
    return [x, y, theta]

## 0.35 0.32 rz = 1.992 rad +- 0.3