import numpy as np
import pandas as pd
import os
import time

import cv2 as cv
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

TEST_SPLIT = 0.2
VALIDATION_SPLIT = 0.2

BATCH_SIZE = 20
IMAGE_SIZE = (100, 100)

ALL_CLASSES = [f"{i}x{j}" for i in range(7) for j in range(0, i + 1)]

DROPOUT = 0.2


def categorized_from_directory(path: str):
    """Returns a Pandas dataframe with the `category` and `path` of each image."""
    rows = []
    for category in os.listdir(path):
        category_path = os.path.join(path, category)
        for image in os.listdir(category_path):
            image_path = os.path.join(category_path, image)
            rows.append({'category': category, 'path': image_path})
    return pd.DataFrame(rows)

def split_data(data):
    # Separar una parte para test
    train_data, test_data = train_test_split(data, test_size=TEST_SPLIT, stratify=data['category'])
    # Dividir el resto en datos de entrenamiento y validación
    train_data, validation_data = train_test_split(train_data, test_size=VALIDATION_SPLIT, stratify=train_data['category'])
    
    return train_data, validation_data, test_data

def flow_from_datagenerator(datagen, data, batch_size=BATCH_SIZE):
    """Returns a generator from an ImageDataGenerator and a dataframe."""
    return datagen.flow_from_dataframe(
        dataframe = data, 
        x_col = "path", 
        y_col = "category", 
        class_mode = 'categorical', 
        batch_size = batch_size,
        target_size = IMAGE_SIZE,
        classes = ALL_CLASSES,
        color_mode = 'grayscale'
    )

def develop_model(data_directory: str, save=True):
    full_data = categorized_from_directory(data_directory)
    
    # Dividir dataset en entrenamiento, validación y test
    train_data, validation_data, test_data = split_data(full_data)
    
    # Obtener el número de categorías totales
    num_categories = len(full_data['category'].unique())
    
    # Crear generadores de datos
    train_datagen = ImageDataGenerator(rescale = 1.0 / 255, rotation_range = 360)
    train_gen = flow_from_datagenerator(train_datagen, train_data)
    train_steps = train_gen.n // train_gen.batch_size
    
    validation_datagen = ImageDataGenerator(rescale=1.0 / 255)
    val_gen = flow_from_datagenerator(validation_datagen, validation_data)
    val_steps = val_gen.n // val_gen.batch_size
    
    test_datagen = ImageDataGenerator(rescale=1.0 / 255)
    test_gen = flow_from_datagenerator(test_datagen, test_data)
    test_steps = test_gen.n // test_gen.batch_size
    
    # Definir el modelo
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu',input_shape=(100, 100, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(DROPOUT),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(DROPOUT),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(num_categories, activation='softmax')
    ])
    
    opt = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
    
    # Entrenamiento del modelo
    t = time.perf_counter()
    history = model.fit(
        train_gen, 
        steps_per_epoch=train_steps, 
        epochs = 100,
        validation_data=val_gen, 
        validation_steps=val_steps,
        verbose=2
    )
    elapsed_time = round((time.perf_counter() - t) / 60, 2)
    print('Training time = ', elapsed_time, 'minutos')
    
    print(f"Se ha alcanzado: accuracy = {history.history['accuracy'][-1]}, val_accuracy = {history.history['val_accuracy'][-1]}")
    if save:
        model.save('model_grayscale_relu_32_64_32.h5')
        
    return model


def piece_recognition(filename: str) -> str:
    """Reconocimiento del tipo de pieza utilizando una red neuronal convolucional

    Args:
        filename (str): Ruta de la imagen a clasificar

    Returns:
        str: Tipo de ficha
    """
    img = cv.imread(filename)
    # cv.imshow("Imagen original", img)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    working_dir = os.path.dirname(os.path.abspath(__file__))
    
    model = load_model(os.path.abspath(os.path.join(working_dir, 'model_grayscale_relu_32_64_32.h5')))
    Y_pred_test = model.predict(gray)
    y_pred_test = np.argmax(Y_pred_test, axis=1)
    return y_pred_test
