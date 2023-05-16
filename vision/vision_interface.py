import os
import cv2 as cv
import time
from datetime import datetime
from typing import List

from .opencv.pieces_recognition_v3 import PiecesIdentifier
from .opencv.pieces_detection_v3 import PiecesDetector
from .opencv.preprocessing import preprocessing_img
from .opencv.piece import Piece

import operator

class DominoVision:
    def __init__(self, visualize=False, verbose=False) -> None:
        self.visualize = visualize
        self.verbose = verbose
        self.pieces = []
        self.PIECE_WIDTH_MM = 19
        self.PIECE_HEIGHT_MM = 38
        
        # Guardar piezas anteriores
        self.pieces_old = []
        self.pieces_tmp = []
        self.coincidences = 0
        self.new_turn = True
        self.flag_changing_turn = False

    def preprocess_img(self, img: cv.Mat, open_size=(1,1)) -> cv.Mat:
        """Preprocesamiento de la imagen, aplicando filtros y operaciones morfológicas

        Args:
            img (Mat): Imagen
            open_size (int, int): Definir el tamaño del kernel para realizar la operación de apertura

        Returns:
            processed_img (Mat): Imagen procesada.
        """
        return preprocessing_img(img, open_size=open_size, visualize=self.visualize)
    
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
        if self.new_turn:
            if len(self.pieces):
                self.pieces_old = self.pieces
            else:
                self.pieces_old = detector.pieces
            self.new_turn = False
        
        self.pieces = detector.pieces
        return self.pieces
    
    def detect_changes(self):
        # is_addition = len(self.pieces) > len(self.pieces_old)
        if len(self.pieces) > len(self.pieces_old):
            pieces_max = self.pieces
            pieces_min = self.pieces_old
        else:
            pieces_max = self.pieces_old
            pieces_min = self.pieces
        
        not_coincidences = [piece_max for piece_max in pieces_max if (not piece_max in pieces_min)]
        is_change = len(not_coincidences) > 0
        if self.verbose:
            if is_change:
                print(f"Se ha producido un cambio en las piezas del juego. Habían {len(self.pieces_old)} fichas y ahora hay {len(self.pieces)}.")
                print(f"{len(not_coincidences)} piezas no coinciden")
            else:
                print("Las piezas son las mismas")

        return is_change
        
    def detect_new_turn(self):
        if self.verbose: print("*"*20, "Comprobando cambio de turno", "*"*20)
        
        # Detección de cambios
        if self.detect_changes():
            self.coincidences = 0
            if not self.flag_changing_turn:
                self.flag_changing_turn = True
            self.new_turn = False
        else:
            self.coincidences += 1
        
        if self.coincidences >= 5:
            if self.flag_changing_turn:
                self.new_turn = True
            self.flag_changing_turn = False
            self.coincidences = 0
            if self.verbose: print("*"*20, "Ha ocurrido un cambio de turno", "*"*20)
            
        else:
            if self.verbose: print("El turno sigue siendo el mismo")
            self.new_turn = False
        return self.new_turn

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
        
        if self.detect_new_turn():
            print("Nuevo turno!")
        
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
        size = width*height
        
        while True:
            _, frame = capture.read()
            if self.visualize:
                cv.imshow('Video', frame)
            # cv.waitKey(0)
            detections = self.pieces_detection(frame, size)
            recognitions = self.pieces_recognition(frame, size, pieces=detections)
            if self.verbose or True:
                if len(recognitions):
                    print(f"Se han reconocido {len(recognitions)} piezas")
                else:
                    print(f"No se ha podido reconocer ninguna pieza")
            
            # if self.detect_new_turn():
            #     print("Nuevo turno!")
            time.sleep(0.5)
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
        
    def view_video(self, channel=1):
        # Capura a partir de la cámara
        capture = cv.VideoCapture(channel)
        while True:
            ret, frame = capture.read()
            if not ret:
                print("Hay un problema con la captura!")
            # else:
            #     print("Captura con éxito")
            cv.imshow('Video', frame)
            time.sleep(0.1)
            if cv.waitKey(20) & 0xFF==ord('d'):
                break
        capture.release()
        cv.waitKey(0)
        cv.destroyAllWindows()

    def ordenar_piezas(self, piezas: Piece):
        """Ordenar piezas de derecha a izquierda, de arriba a abajo. 

        Args:
            piezas
        """
        longitud = max(piezas[0].size)
        piezas_ordenadas = []

        # ordenar en función de su horizontal
        valor_horizontal = [pieza.center[0] for pieza in piezas]
        ind_orden = sorted(range(len(piezas)), key=lambda k: valor_horizontal[k]) # stack overflow
        piezas_ordenadas_dcha_a_izda = [piezas[ind_orden[-i-1]] for i in range(len(piezas))] # orden inverso porque no sé cómo hacerlo

        piezas_misma_vertical = []
        
        for pieza in piezas_ordenadas_dcha_a_izda:   
            if not piezas_misma_vertical:
                piezas_misma_vertical.append(pieza)
            elif abs(pieza.center[0] - piezas_misma_vertical[0].center[0]) < longitud:
                piezas_misma_vertical.append(pieza)
            else:
                # ordenar subgrupos de piezas de misma horizontal, en función de su vertical
                valor_vertical = [pieza_mv.center[1] for pieza_mv in piezas_misma_vertical]
                ind_orden = sorted(range(len(piezas_misma_vertical)), key=lambda k: valor_vertical[k])
                piezas_ordenadas_arriba_a_abajo = [piezas_misma_vertical[ind_orden[i]] for i in range(len(piezas_misma_vertical))]
                piezas_ordenadas.extend(piezas_ordenadas_arriba_a_abajo)
                piezas_misma_vertical = [pieza]

        # una última vez ordenar en función de su vertical
        valor_vertical = [pieza_mv.center[1] for pieza_mv in piezas_misma_vertical]
        ind_orden = sorted(range(len(piezas_misma_vertical)), key=lambda k: valor_vertical[k])
        piezas_ordenadas_arriba_a_abajo = [piezas_misma_vertical[ind_orden[i]] for i in range(len(piezas_misma_vertical))]
        piezas_ordenadas.extend(piezas_ordenadas_arriba_a_abajo)

        return piezas_ordenadas

