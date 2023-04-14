import os
import cv2 as cv
from opencv.pieces_recognition_v1 import pieces_recognition
from opencv.pieces_detection_v1 import pieces_detection
import time
from datetime import datetime


# tamaño fichas: 3.8x1.9 cm

def test_with_image(filename):
    img = cv.imread(filename)
    cv.imshow("Imagen real", img)
    recognitions = pieces_recognition(img, size=img.shape[0]*img.shape[1], preprocess=True, verbose=False, visualize=True)
    # detections = pieces_detection(img, size=img.shape[0]*img.shape[1], preprocess=True, verbose=False, visualize=True)
    if len(recognitions):
        print(f"Se han reconocido {len(recognitions)} piezas")
        # print(recognitions)
    else:
        print(f"No se ha podido reconocer ninguna pieza")
    cv.waitKey(0)
    cv.destroyAllWindows()

def test_with_video(channel=1):
    # Capura a partir de la cámara
    capture = cv.VideoCapture(1)

    width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)

    while True:
        ret, frame = capture.read()
        cv.imshow('Video', frame)
        recognitions = pieces_recognition(frame, size=width*height, verbose=False, visualize=True)
        # detections = pieces_detection(img, size=img.shape[0]*img.shape[1], preprocess=True, verbose=False, visualize=True)
        if len(recognitions):
            print(f"Se han reconocido {len(recognitions)} piezas")
            print(recognitions)
        else:
            print(f"No se ha podido reconocer ninguna pieza")
        time.sleep(0.2)
        if cv.waitKey(20) & 0xFF==ord('d'):
            break
    capture.release
    cv.waitKey(0)
    cv.destroyAllWindows()
    
def save_img(img):
    now = datetime.now()
    filename_dest = "fotos_ur3/" + now.strftime("%Y%m%d_%H%M%S") + ".jpg"
    cv.imwrite(filename_dest, img)


path_dir = "fotos_ur3/"
filename = os.path.join(path_dir, "20230412_194329.jpg")
test_with_image(filename)