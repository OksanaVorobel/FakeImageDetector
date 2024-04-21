import os

import keras
import tensorflow as tf
from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D

from app.core.config import model_config


def scheduler(epoch, lr):
    lr_0 = lr
    lr_max = 0.001
    lr_0_steps = 5
    lr_max_steps = 5
    lr_min = 0.0005
    lr_decay = 0.9
    if epoch < lr_0_steps:
        lr = lr_0 + ((lr_max - lr_min) / lr_0_steps) * (epoch - 1)
    elif epoch < lr_0_steps + lr_max_steps:
        lr = lr_max
    else:
        lr = max(lr_max * lr_decay ** (epoch - lr_0_steps - lr_max_steps), lr_min)
    return lr


data_augmentation = tf.keras.Sequential(
    [
        layers.RandomFlip(
            "horizontal",
            input_shape=(model_config.img_height, model_config.img_width, 3)
        ),
        # yers.RandomRotation(0.01),
        layers.RandomZoom(0.1),
    ])


def get_model():
    if os.path.exists(f'./{model_config.model_file_name}'):
        return keras.models.load_model(f'./{model_config.model_file_name}')

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
