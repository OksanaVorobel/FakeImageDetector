import tensorflow as tf
from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D

from app.core.config import model_config
from app.utils.utils import load_fake_detection_model


data_augmentation = tf.keras.Sequential(
    [
        layers.RandomFlip(
            "horizontal",
            input_shape=(model_config.img_height, model_config.img_width, 3)
        ),
        layers.RandomRotation(0.01),
        layers.RandomZoom(0.1),
    ])


def get_model():
    if cnn := load_fake_detection_model():
        return cnn

    cnn = Sequential()
    cnn.add(
        Conv2D(filters=32, kernel_size=(5, 5), padding='valid', activation='relu',
               input_shape=(model_config.img_height, model_config.img_width, 3)))
    cnn.add(
        Conv2D(filters=32, kernel_size=(5, 5), padding='valid', activation='relu'))
    cnn.add(MaxPool2D(pool_size=(2, 2)))
    cnn.add(Dropout(0.25))
    cnn.add(Flatten())
    cnn.add(Dense(256, activation="relu"))
    cnn.add(Dropout(0.5))
    cnn.add(Dense(2, activation="softmax"))

    cnn.summary()
    return cnn


model = get_model()
