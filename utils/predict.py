from keras.preprocessing.image import img_to_array
from keras.applications.vgg19 import preprocess_input
import tensorflow as tf
import numpy as np
import pickle
import sys

sys.path.append('..')
from utils.config import Config, load_trained_model, load_trained_classes


def preprocess_image(image):
    if image.mode != "RGB":
        image.convert("RGB")

    image = image.resize(Config.TARGET_SIZE)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    return image


def predict(image, entity_name, model_name, model_iteration):
    if (Config.MODEL == None) or (Config.DEFAULT_GRAPH == None):
        return

    if entity_name != Config.ENTITY_NAME or\
            model_name != Config.MODEL or \
            model_iteration != Config.ITERATION:

        load_trained_model(
            f"data/{entity_name}/{model_name}_{model_iteration}.model")
        load_trained_classes(
            f"data/{entity_name}/{model_name}_{model_iteration}_classes.p")

    image = preprocess_image(image)

    with Config.DEFAULT_GRAPH.as_default():
        preds = Config.MODEL.predict(image)

    return preds