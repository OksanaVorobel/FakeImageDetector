import logging
import os

import cv2
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
from pylab import array
from keras.utils import to_categorical

from app.core.config import model_config
from app.utils.utils import convert_to_ela_image

path_original = './CASIA2/Au/'
path_tampered = './CASIA2/Tp/'

total_original = os.listdir(path_original)
total_tampered = os.listdir(path_tampered)


def get_imlist(path):
    return [os.path.join(path, f) for f in os.listdir(path) if
            f.endswith('.jpg') or f.endswith('.JPG') or f.endswith('.png') or f.endswith('.tif')]


def get_all_images():
    images = []
    for file in tqdm(os.listdir(path_original)):
        try:
            if file.endswith('jpg') or file.endswith('JPG') or file.endswith('jpeg') or file.endswith('JPEG'):
                if int(os.stat(path_original + file).st_size) > 10000:
                    line = path_original + file + ',0\n'
                    images.append(line)
        except:
            print(path_original + file)

    for file in tqdm(os.listdir(path_tampered)):
        try:
            if file.endswith('jpg'):
                if int(os.stat(path_tampered + file).st_size) > 10000:
                    line = path_tampered + file + ',1\n'
                    images.append(line)
            if file.endswith('tif'):
                if int(os.stat(path_tampered + file).st_size) > 10000:
                    line = path_tampered + file + ',1\n'
                    images.append(line)
        except:
            print(path_tampered + file)

    return images


def convert_origin_image(path):
    original_image = cv2.imread(path)
    # Зміна розміру зображення
    resized_image = cv2.resize(original_image, (model_config.img_height, model_config.img_width))
    # Нормалізація значень пікселів (ділення на 255)
    normalized_image = resized_image / 255.0
    return normalized_image

def get_ela_split_data() -> tuple[np.array, np.array]:
    if os.path.exists("./cnn_model/ela_values.npy") and os.path.exists("./cnn_model/ela_labels.npy"):
        logging.info("loading dataset...")
        XX = np.load("./cnn_model/ela_values.npy")
        YY = np.load("./cnn_model/ela_labels.npy")
    else:
        logging.info("Image arrays could not be found, creating new ones...")
        X = []
        Y = []
        for index, row in tqdm(dataset.iterrows()):
            X.append(array(
                convert_to_ela_image(row[0], 90)
                .resize((model_config.img_height, model_config.img_width), resample=Image.LANCZOS)
            ).flatten() / 255.0)
            Y.append(row[1])

        XX = np.array(X)
        XX = XX.reshape(-1, model_config.img_height, model_config.img_width, 3)
        YY = to_categorical(Y, 2)
        del X
        del Y

        np.save("cnn_model/ela_values", XX)
        np.save("cnn_model/ela_labels", YY)

    return XX, YY


def get_origin_split_data():
    X = []
    Y = []
    for index, row in tqdm(dataset.iterrows()):
        X.append(convert_origin_image(row[0]))
        Y.append(row[1])

    if os.path.exists("./cnn_model/original_values") and os.path.exists("./cnn_model/original_labels"):
        XX = np.load("./cnn_model/original_values.npy")
        YY = np.load("./cnn_model/original_labels.npy")
    else:
        X = []
        Y = []
        for index, row in tqdm(dataset.iterrows()):
            X.append(convert_origin_image(row[0]))
            Y.append(row[1])

        XX = np.array(X)
        XX = XX.reshape(-1, model_config.img_height, model_config.img_width, 3)
        YY = to_categorical(Y, 2)
        del X
        del Y

        np.save("cnn_model/original_values", XX)
        np.save("cnn_model/original_labels", YY)

    return XX, YY


def create_dataset():
    if os.path.exists("./dataset_CASIA2.csv"):
        dataset = pd.read_csv('./dataset_CASIA2.csv')
    else:
        images = get_all_images()
        image_name = []
        label = []
        for i in tqdm(range(len(images))):
            image_name.append(images[i][0:-3])
            label.append(images[i][-2])

        dataset = pd.DataFrame({'image': image_name, 'class_label': label})
        dataset.to_csv('dataset_CASIA2.csv', index=False)

    return dataset


dataset = create_dataset()
