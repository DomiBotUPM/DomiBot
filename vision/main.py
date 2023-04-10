import os
import cv2 as cv
from opencv.piece_recognition_v2 import piece_recognition
import time

# path_dir = "dataset_fichas/"
# filename = os.path.join(path_dir, "6x5/20180505_181840.jpg")
# img = cv.imread(filename)

# Capura a partir de la cámara
capture = cv.VideoCapture(0)

width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)

while True:
    _, frame = capture.read()
    cv.imshow('Video', frame)
    success, type_piece = piece_recognition(frame, size=width*height)
    if success:
        print(f"La ficha es de tipo {type_piece}")
    else:
        print(f"No se ha podido reconocer la pieza")
    time.sleep(2)
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release



cv.destroyAllWindows()
