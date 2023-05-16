import os
from vision.vision_interface import DominoVision
import cv2 as cv
import sys

width_game = 236
height_game = 314
area_game = width_game*height_game
domino_vision = DominoVision(visualize=True, verbose=True)

# Probar directamente desde la camara
# domino_vision.test_with_video(channel=0, size_mm=area_game)
# domino_vision.view_video(channel=0)

# Probar con imagenes

# path_dir = os.path.abspath("vision/fotos_ur3/")
# i = 0
# for file in os.listdir(path_dir)[:]:
#     filename = os.path.join(path_dir, file)
#     domino_vision.test_with_image(filename)
#     cv.waitKey(0)

# Probar con una imagen tomada en el momento
capture = cv.VideoCapture(0)

width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
size = width*height

ret, frame = capture.read()
if not ret:
    sys.exit("No se ha podido tomar una captura")

cv.imshow('Video', frame)
print(f"Area px: {size}. Area mm^2: {area_game}")
detections = domino_vision.pieces_detection(frame, size, size_mm=area_game)
# recognitions = domino_vision.pieces_recognition(frame, size, pieces=detections)
# if len(recognitions):
#     print(f"Se han reconocido {len(recognitions)} piezas")
# else:
#     print(f"No se ha podido reconocer ninguna pieza")

capture.release()
cv.waitKey(0)
cv.destroyAllWindows()
