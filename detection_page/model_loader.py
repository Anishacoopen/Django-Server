# image_classification/model_loader.py
import os
from tensorflow import keras

def load_model():
    model_path = 'C:/Users/Anisha/DjangoUI/DisasterDetection/Models(H5 Format)/Final_Best_InceptionV3_True.h5'
    model = keras.models.load_model(model_path)
    return model