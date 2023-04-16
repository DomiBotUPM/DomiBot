import os
import cv2 as cv
from opencv.piece_recognition_v2 import piece_recognition
from opencv.pieces_recognition_v1 import pieces_recognition
from opencv.pieces_detection_v1 import pieces_detection
from opencv.pieces_location import pieces_location
import time
from datetime import datetime


# tamaño fichas: 3.8x1.9 cm

def test_piece(filename):
    img = cv.imread(filename)
    cv.imshow("Imagen real", img)
    img_i = img.copy()
    recognition = piece_recognition(img_i)
    if len(recognition):
        print(f"La pieza es de tipo {recognition}")
    else:
        print(f"No se ha podido reconocer ninguna pieza")
    cv.waitKey(0)
    cv.destroyAllWindows()


def test_with_image(filename, visualize=True):
    img = cv.imread(filename)
    cv.imshow("Imagen real", img)
    recognitions = pieces_recognition(img, size=img.shape[0]*img.shape[1], preprocess=True, visualize=visualize)
    detections = pieces_detection(img, size=img.shape[0]*img.shape[1], preprocess=True, visualize=visualize)
    if len(recognitions):
        print(f"Se han reconocido {len(recognitions)} piezas")
        locations = pieces_location(recognitions, img=img, visualize=visualize)
        for loc in locations:
            print(loc)
        # print(recognitions)
    else:
        print(f"No se ha podido reconocer ninguna pieza")
    cv.waitKey(0)
    cv.destroyAllWindows()

def test_with_video(channel=1, visualize=True):
    # Capura a partir de la cámara
    capture = cv.VideoCapture(channel)

    width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)

    while True:
        ret, frame = capture.read()
        cv.imshow('Video', frame)
        recognitions = pieces_recognition(frame, size=width*height, preprocess=True, visualize=visualize)
        detections = pieces_detection(frame, size=width*height, preprocess=True, visualize=visualize)
        if len(recognitions):
            print(f"Se han reconocido {len(recognitions)} piezas")
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



# Probar directamente desde la cámara
# test_with_video(channel=1)

# Probar con imagen
path_dir = "fotos_ur3/"

for file in os.listdir(path_dir)[0:5]:
    filename = os.path.join(path_dir, file)
    test_with_image(filename)

