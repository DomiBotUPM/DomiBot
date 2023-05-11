import cv2 as cv

def preprocessing_img(img: cv.Mat, open_size=(1,1), visualize=False) -> cv.Mat:
    """Preprocesamiento de la imagen, aplicando filtros y operaciones morfológicas

    Args:
        img (Mat): Imagen
        open (int): Definir el tamaño del kernel para realizar la operación de apertura
        visualize (bool, optional): Definir si se quiere visualizar o no las imágenes resultantes. Defaults to False.

    Returns:
        processed_img: Imagen procesada.
    """
    # img[:,:,1] = 0
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (1,1), cv.BORDER_DEFAULT)
    
    thresh, binarized = cv.threshold(blur, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, open_size)
    morph_img = cv.morphologyEx(binarized, cv.MORPH_OPEN, kernel, iterations=5)
    
    if visualize:
        cv.imshow("Escala de grises", gray)
        cv.imshow(f"Imagen binarizada con umbral: {thresh}", binarized)
        cv.imshow(f"Imagen binarizada tras apertura de {open}", morph_img)
    
    return morph_img