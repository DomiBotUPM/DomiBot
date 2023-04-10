import os
import cv2 as cv
from opencv.piece_recognition_v2 import piece_recognition

path_dir = "dataset_fichas/"
filename = os.path.join(path_dir, "6x5/20180505_181840.jpg")
img = cv.imread(filename)

# Capura a partir de la cámara
# capture = cv.VideoCapture(0)
# _, img = capture.read()
# while True:
#     _, frame = capture.read()
#     cv.imshow('Video', frame)

#     if cv.waitKey(20) & 0xFF==ord('d'):
#         break
# capture.release

type_piece = piece_recognition(img)
print(f"La ficha es de tipo {type_piece}")

cv.destroyAllWindows()
