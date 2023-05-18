import os
from vision.vision_interface import DominoVision
import cv2 as cv
import sys

width_game = 236
height_game = 314
area_game = width_game*height_game
domino_vision = DominoVision(visualize=True, verbose=True)

# Probar con imagenes guardadas
def images_offline():
    path_dir = os.path.abspath("vision/fotos_ur3/")
    i = 0
    for file in os.listdir(path_dir)[:]:
        filename = os.path.join(path_dir, file)
        domino_vision.test_with_image(filename)
        cv.waitKey(0)
        cv.destroyAllWindows()

# Probar con una imagen tomada en el momento
def images_online():
    capture = cv.VideoCapture(0)

    width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
    size = width*height

    ret, frame = capture.read()
    if not ret:
        sys.exit("No se ha podido tomar una captura")

    cv.imshow('Imagen', frame)
    # detections = domino_vision.pieces_detection(frame, size, size_mm=0.0)
    recognitions = domino_vision.pieces_recognition(frame, size, pieces=[])

    capture.release()
    cv.waitKey(0)
    cv.destroyAllWindows()

images_online()