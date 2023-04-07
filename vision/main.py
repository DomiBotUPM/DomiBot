import os
from opencv.piece_recognition_v1 import piece_recognition

path_dir = "dataset_fichas/"
filename = os.path.join(path_dir, "6x3/20180505_180841.jpg")

type_piece = piece_recognition(filename)
print(f"La ficha es de tipo {type_piece}")
