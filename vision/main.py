import os
import cv2 as cv
from opencv.piece_recognition_v1 import piece_recognition

# path_dir = "dataset_fichas/"
# filename = os.path.join(path_dir, "5x4/20180505_181205.jpg")
# img = cv.imread(filename)

capture = cv.VideoCapture(0)
_, img = capture.read()
capture.release
print(img.shape)
type_piece = piece_recognition(img)
print(f"La ficha es de tipo {type_piece}")

cv.destroyAllWindows()
