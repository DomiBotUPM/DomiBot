import cv2 as cv
from typing import List, Tuple
import numpy as np
import math

from .preprocessing import preprocessing_img
from .piece import Piece


class PiecesDetector:
    def __init__(self, img, size, size_mm = 0.0, preprocess=True, verbose=False, visualize=False):
        """Inicializar detector de piezas

        Args:
            img (Mat): Imagen
            size (float): Area de la imagen total en pixeles
            preprocess (bool, optional): Realizar preprocesamiento de la imagen. Defaults to False.
            verbose (bool, optional): Mostrar mensajes de seguimiento. Defaults to False.
            visualize (bool, optional): Visualizar imagenes intermedias. Defaults to False.
        """
        self.img = img
        self.size = size
        self.preprocess = preprocess
        self.verbose = verbose
        self.visualize = visualize
        self.pieces = []
        self.PIECE_WIDTH_MM = 19
        self.PIECE_HEIGHT_MM = 38
        
        self.processed_img = self.__preprocess_img(img)
        # Si nos dan el tamano fisico, podemos obtener directamente el ratio px/mm y el area de una pieza estandar en pixeles
        if size_mm > 0:
            self.ratio_px2mm = np.sqrt(size_mm / size)
            self.ref_piece_area = (self.PIECE_WIDTH_MM * self.PIECE_HEIGHT_MM) / (self.ratio_px2mm**2)
        else:
            self.ratio_px2mm = 0.0
            self.ref_piece_area = 0.0
    
    def __preprocess_img(self, img):
        img_i = img.copy()
        if self.preprocess:
            return preprocessing_img(img_i, visualize=False)
        else:
            return img_i
    
    def get_ratio_px2mm_from_piece(self, piece):
        """Obtener el ratio de conversion de pixeles a milimetros, a partir de una pieza. 

        Args:
            piece (Piece): Objeto de clase Piece

        Returns:
            float: Ratio de conversion px --> mm
        """
        width = min(piece.size[0], piece.size[1])
        return self.PIECE_WIDTH_MM / width
        
    def change_img(self, new_img, new_size):
        self.img = new_img
        self.size = new_size
        
    def set_ratio_px2mm(self, ratio):
        self.ratio_px2mm = ratio
        
    def get_angle_from_box(self, box):
        # Obtenemos primero el vertice que se encuentra mas abajo
        idx_lower_vertex = box[:, 1].argsort()[::-1][0]
        num_vertex = len(box[:, 0])
        # Obtenemos sus vecinos
        neighbour_indexes = [idx_lower_vertex-1, idx_lower_vertex+1]
        if neighbour_indexes[0] < 0:
            neighbour_indexes[0] = num_vertex - 1
        elif neighbour_indexes[1] >= num_vertex:
            neighbour_indexes[1] = 0
        
        # Obtenemos el vecino mas alejado para seguir siempre el mismo criterio
        dist_max = 0
        idx_max_dist = -1
        for idx in neighbour_indexes:
            distance = math.dist(box[idx], box[idx_lower_vertex])
            if distance > dist_max:
                dist_max = distance
                idx_max_dist = idx
        
        # Calculamos el angulo a partir de la tangente dy/dx
        dy = box[idx_lower_vertex,1] - box[idx_max_dist,1]
        dx = box[idx_max_dist,0] - box[idx_lower_vertex,0]
        angle = np.rad2deg(np.arctan2(dy,dx))
        
        if self.verbose: print("Angulo a partir de contorno rectangular:", round(angle,2))
        
        return angle
    
    def detect_pieces(self):
        """Deteccion de las fichas de domino presentes en la zona

        Returns:
            List[Piece]: Lista de piezas detectadas.
        """
        if self.verbose: print("*"*20, "Se ha iniciado la deteccion de piezas", "*"*20)
        img_i = self.img.copy()
        
        # Detectar contornos
        contours, _ = cv.findContours(self.processed_img, mode=cv.RETR_CCOMP, method=cv.CHAIN_APPROX_SIMPLE)
        filtered_contours = [contour for contour in contours if cv.contourArea(contour) > 1.6e-4*self.size] # Minima area para un punto
        
        # Si no hay ningun contorno minimamente grande, se finaliza la deteccion
        if len(filtered_contours) == 0:
            if self.verbose: print("No se ha detectado ningun contorno minimamente grande")
            return []
        
        # Encontrar solo los contornos que sean de piezas
        pieces = []
        if self.ref_piece_area > 0:
            min_area_piece = 0.8*self.ref_piece_area
        else:
            min_area_piece = 7e-3*self.size
        
        if self.verbose: print("Tamano de referencia para detectar pieza:", min_area_piece)
        # ########## COMIENZO DE CAMBIOS DE PABLO ##########
        for contour in filtered_contours:
            area = cv.contourArea(contour)
            # El tamano minimo para un punto
            if area < 1.6e-4*self.size:
                continue
            center, (width,height), angle = cv.minAreaRect(contour)
            ratio = width/height
            # Para que sea una pieza el ancho debe ser la mitad que el alto y debe ser al menos de un tamano concreto
            cond_width_rectangle = min(width, height) > np.sqrt(min_area_piece/2)
            if area > min_area_piece and cond_width_rectangle: # Buscamos que al menos su area y su ancho sean de un tamaño minimo
                box = np.int64(cv.boxPoints((center, (width,height), angle)))
                mask = np.zeros(self.processed_img.shape, np.uint8)
                cv.fillPoly(mask, [box], color=(255))
                angle = self.get_angle_from_box(box)
                pieces.append(Piece(mask, box, np.round(center,3), angle, size=(round(width,3), round(height,3))))
                if self.verbose: print("Area del contorno:", area, ". Area del rectangulo:", round(width,1), "*", round(height,1), " =", round(width*height,2), "Angulo:", angle)
        
        if self.verbose: print("NO de elementos:", len(filtered_contours), ". NO de candidatos a piezas:", len(pieces))
        
        # Si no se ha encontrado ningun candidato a pieza, se finaliza la deteccion
        if len(pieces) == 0:
            return pieces
        
        if self.verbose: print("Se procede a buscar piezas anomalas")
        
        # Si no se tiene la referencia del tamano de una pieza, se calcula la media
        if self.ref_piece_area > 0:
            ref_area =self.ref_piece_area
        else:
            ref_area = round(np.mean([piece.get_area() for piece in pieces]),2)
        
        pieces_big = [p for p in pieces if p.get_area() >= 1.5*ref_area]
        pieces = [p for p in pieces if p.get_area() < 1.5*ref_area]
        
        if self.visualize: 
            for piece in pieces:
                cv.drawContours(img_i,[piece.contour],0,(255,0,0), thickness=2)
        
        # Se procede a aplicar otro algoritmo para los casos en que haya piezas juntas y las detecte como una sola
        if len(pieces_big):
            if self.ratio_px2mm == 0.0:
                self.ratio_px2mm = self.get_ratio_px2mm_from_piece(pieces[0])
                if self.verbose: print("Pieza utilizada como referencia para ratio. Ancho:", min(pieces[0].size[0], pieces[0].size[1]), ". Ratio:", round(self.ratio_px2mm, 2))
            for i, piece in enumerate(pieces_big):
                if self.verbose: 
                    print("Indice de pieza actual:", i)
                    print("Se ha encontrado una pieza anomala de tamano:", piece.get_area(), ". Tamano de pieza de referencia:", ref_area, ".")
                
                # Se separa la "pieza" detectada como una sola, en las verdaderas que habia
                split_pieces = self.split_piece(piece)
                for piece in split_pieces:
                    pieces.append(piece)
                    if self.visualize:
                        cv.drawContours(img_i,[piece.contour],0,(0,255,0), thickness=2)
        
            if self.verbose:  print("NO de elementos:", len(contours), ". NO de piezas detectadas:", len(pieces))
        if self.visualize: cv.imshow("Deteccion de piezas", img_i)
        
        self.pieces = pieces
        
        if self.verbose: print("*"*20, "Se ha finalizado la deteccion de piezas", "*"*20)
        return pieces
    
    def split_piece(self, piece):
        """Division de una pieza anormalmente grande en sus respectivas internas

        Returns:
            List[Piece]: Lista de piezas detectadas.
        """
        print("splitear")

        if self.verbose: print("-"*5, "Se inicia la separacion de piezas", "-"*5)
        
        masked = cv.bitwise_and(self.processed_img, piece.mask)
        # Detectar contornos
        contours, _ = cv.findContours(masked, mode=cv.RETR_CCOMP, method=cv.CHAIN_APPROX_SIMPLE)
        filtered_contours = [contour for contour in contours if cv.contourArea(contour) > 1.6e-4*self.size] # Minima area para un punto
        # Encontrar solo las lineas separadoras de las piezas
        pieces = []
        for contour in filtered_contours:
            area = cv.contourArea(contour)
            center, (width,height), angle = cv.minAreaRect(contour)
            ratio = min(width,height)/max(width,height)
            
            # Condicion de tamano de la linea separadora si tenemos la referencia del tamano de pieza
            if self.ref_piece_area > 0:
                cond_size = max(width, height) > 0.5*(self.ratio_px2mm*self.PIECE_WIDTH_MM) and width*height < 0.25*self.ref_piece_area
            else: # Si no tenemos la referencia
                cond_size = width*height < 1e-2*self.size
            
            # ########## COMIENZO DE CAMBIOS DE PABLO ##########
            # Para que sea una linea separadora el ratio debe ser muy pequeno o muy grande
            if ratio < 0.3 and cond_size:
                box = np.int64(cv.boxPoints((center, (width,height), angle)))
                mask = np.zeros(self.processed_img.shape, np.uint8)
                cv.fillPoly(mask, [box], color=(255))
                
                if self.verbose: print("Encontrada linea separadora de", round(width,2), "x", round(height,2), "=", round(width*height,2))
                # Con ayuda del ratio, se obtiene el contorno de la pieza
                if width > height: # Horizontal
                    new_width = 19/self.ratio_px2mm
                    new_height = 38/self.ratio_px2mm
                else: # Vertical
                    new_width = 38/self.ratio_px2mm
                    new_height = 19/self.ratio_px2mm
                
                box_piece = np.int64(cv.boxPoints((center, (new_width,new_height), angle)))
                new_mask = np.zeros(self.processed_img.shape, np.uint8)
                cv.fillPoly(new_mask, [box_piece], color=(255))
                true_angle = self.get_angle_from_box(box_piece)
                pieces.append(Piece(new_mask, box_piece, np.round(center,3), true_angle, size=(round(new_width,3), round(new_height,3))))
                if self.verbose: print("Nueva pieza encontrada. Area de la linea separadora:", area, ". Area de la pieza:", round(new_width,1), "*", round(new_height,1), " =", round(new_width*new_height,2), "Angulo:", true_angle)
                # ########## FIN DE CAMBIOS DE PABLO ##########
        if self.verbose: print("Num de elementos:", len(filtered_contours), ". Num de piezas detectadas:", len(pieces))
        # if self.visualize: cv.imshow("Separacion de piezas en el juego", img_i)
        
        if self.verbose: print("-"*5, "Se finaliza la separacion de piezas", "-"*5)
        return pieces
    
    def locate_piece(self, piece, img=None, copy_img=True):
        """Localizar la pieza con respecto a la imagen o captura realizada

        Args:
            piece (dict): Datos de pieza. Contendra al menos el centro y el tamano en pixeles, asi como el angulo de rotacion.
            img (Mat, optional): Imagen para visualizar. Si no se indica utiliza la que tiene el detector.
            copy_img (bool): Indica si se sobreescribe sobre la imagen o se carga una nueva

        Returns:
            Tuple[float, Tuple[float,float], float]: Centro, tamano en mm, y angulo de rotacion
        """
        if img is not None:
            img_i = img
        else:
            img_i = self.img
        if copy_img:
            img_i = img_i.copy()
        if type(piece) == list:
            print(piece)
        
        center = np.round(self.ratio_px2mm * piece.center, 2)
        width = round(self.ratio_px2mm * piece.size[0], 2)
        height = round(self.ratio_px2mm * piece.size[1], 2)
        if self.visualize and img_i is not None:
            cx = round(piece.center[0])
            cy = round(piece.center[1])
            cv.rectangle(img_i, (cx-48, cy-6), (cx+48, cy+6), (255,255,255), thickness=-1)
            cv.putText(img_i, "(" + str(round(piece.center[0],1)) + "," + str(round(piece.center[1],1))+ "), " + str(round(piece.angle,1)) , (cx-47, cy+3), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0), 1, cv.LINE_AA)
            cv.imshow("Localizacion de piezas", img_i)
        
        return center, (width, height), piece.angle

    def locate_pieces(self):
        """Localizar la pieza con respecto a la imagen o captura realizada
        
        Returns:
            List[Tuple[float, Tuple[float,float], float]]: Lista de localizaciones. Indica: centro en mm, (ancho,alto) en mm y angulo de rotacion en O.
        """
        if not len(self.pieces):
            return []
        img_i = self.img.copy()
        
        # Ratio de conversion px --> mm
        if self.ratio_px2mm == 0.0:
            self.ratio_px2mm = self.get_ratio_px2mm_from_piece(self.pieces[0])
            
        locations = []
        for i, piece in enumerate(self.pieces):
            location = self.locate_piece(piece, img_i, copy_img=False)
            self.pieces[i].center_mm =  location[0]
            self.pieces[i].size_mm = location[1]
            locations.append(location)
        return locations