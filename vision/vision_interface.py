import os
import cv2 as cv
import time
from datetime import datetime
from typing import List

from .opencv.pieces_recognition_v3 import PiecesIdentifier
from .opencv.pieces_detection_v3 import PiecesDetector
from .opencv.preprocessing import preprocessing_img
from .opencv.piece import Piece

class DominoVision:
    def __init__(self, visualize=False, verbose=False) -> None:
        self.visualize = visualize
        self.verbose = verbose
        self.pieces = []
        self.PIECE_WIDTH_MM = 19
        self.PIECE_HEIGHT_MM = 38

    def preprocess_img(self, img: cv.Mat, open=(1,1)) -> cv.Mat:
        """Preprocesamiento de la imagen, aplicando filtros y operaciones morfológicas

        Args:
            img (Mat): Imagen
            open (int): Definir el tamaño del kernel para realizar la operación de apertura

        Returns:
            processed_img (Mat): Imagen procesada.
        """
        return preprocessing_img(img, visualize=self.visualize)
    
    def pieces_recognition(self, img: cv.Mat, size: float, pieces=[], preprocess=True):
        """Identificacion de piezas

        Returns:
            List[dict]: Lista de piezas reconocidas.
        """
        identifier = PiecesIdentifier(img, size, pieces, preprocess=preprocess, visualize=self.visualize, verbose=self.verbose)
        self.pieces = identifier.pieces_recognition()
        return self.pieces
    
    def pieces_detection(self, img: cv.Mat, size: float, preprocess=True) -> List[Piece]:
        """Deteccion de las fichas de domino presentes en la zona

        Returns:
            List[Piece]: Lista de piezas detectadas.
        """
        detector = PiecesDetector(img, size=size, preprocess=preprocess, visualize=self.visualize, verbose=self.verbose)
        detector.detect_pieces()
        detector.locate_pieces()
        self.pieces = detector.pieces
        return self.pieces
    

    def test_with_image(self, filename: str) -> None:
        """Test rápido con una imagen. Se realizan tanto detecciones como reconocimientos

        Args:
            filename (str): Ruta del archivo de la imagen
        """
        img = cv.imread(filename)
        if self.visualize:
            cv.imshow("Imagen real", img)
        size = img.shape[0]*img.shape[1]
        detections = self.pieces_detection(img, size)
        recognitions = self.pieces_recognition(img, size, pieces=detections)
        if len(recognitions):
            print(f"Se han reconocido {len(recognitions)} piezas")
        else:
            print(f"No se ha podido reconocer ninguna pieza")
        cv.waitKey(0)
        cv.destroyAllWindows()

    def test_with_video(self, channel=1) -> None:
        """Test rápido en tiempo real. Se realizan tanto detecciones como reconocimientos cíclicamente.

        Args:
            channel (int, optional): Se indica la cámara a utiizar
        """
        # Capura a partir de la cámara
        capture = cv.VideoCapture(channel)

        width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
        height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
        size = width^height
        
        while True:
            _, frame = capture.read()
            if self.visualize:
                cv.imshow('Video', frame)
            detections = self.pieces_detection(frame, size)
            recognitions = self.pieces_recognition(frame, size, pieces=detections)
            if len(recognitions):
                print(f"Se han reconocido {len(recognitions)} piezas")
            else:
                print(f"No se ha podido reconocer ninguna pieza")
            time.sleep(0.2)
            if cv.waitKey(20) & 0xFF==ord('d'):
                break
        capture.release()
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    def save_img(self, img: cv.Mat) -> None:
        """Guardar imagen. Se guardara en la carpeta vision/fotos_ur3.

        Args:
            img (Mat): imagen a guardar
        """
        now = datetime.now()
        working_dir = os.path.dirname(os.path.abspath(__file__))
        dir_dest = os.path.join(working_dir, "fotos_ur3/")
        filename_dest = dir_dest + now.strftime("%Y%m%d_%H%M%S") + ".jpg"
        cv.imwrite(filename_dest, img)