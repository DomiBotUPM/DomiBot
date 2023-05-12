import os
from vision.vision_interface import DominoVision
import cv2 as cv

domino_vision = DominoVision(visualize=True, verbose=True)

# Probar directamente desde la cámara
# domino_vision.test_with_video(channel=1)
# domino_vision.view_video(channel=1)

capture = cv.VideoCapture(1)

ret, frame = capture.read()


cv.imshow('Video', frame)

cv.waitKey(0)

print('a')

domino_vision.save_img(frame)

# Probar con imagenes
path_dir = os.path.abspath("vision/fotos_ur3/")
i = 0
for file in os.listdir(path_dir)[:]:
    filename = os.path.join(path_dir, file)
    domino_vision.test_with_image(filename)
    cv.waitKey(0)
    