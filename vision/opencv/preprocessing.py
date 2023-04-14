import cv2 as cv

def preprocessing_img(img: cv.Mat, visualize=False):
    """Preprocesamiento de la imagen, aplicando filtros y operaciones morfológicas

    Args:
        img (Mat): Imagen
        visualize (bool, optional): Definir si se quiere visualizar o no las imágenes intermedias. Defaults to False.

    Returns:
        processed_img: Imagen procesada.
    """
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # blur = cv.GaussianBlur(gray, (3,3), cv.BORDER_DEFAULT)
    
    thresh, binarized = cv.threshold(gray, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
    morph_img = cv.morphologyEx(binarized, cv.MORPH_CLOSE, kernel)
    
    if visualize:
        cv.imshow("Escala de grises", gray)
        cv.imshow(f"Imagen binarizada con umbral: {thresh}", binarized)
        cv.imshow(f"Imagen binarizada tras apertura", morph_img)
    
    return morph_img