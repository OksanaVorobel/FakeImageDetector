import os

import keras
from PIL import Image, ImageChops, ImageEnhance

from app.core.config import model_config


def convert_to_ela_image(filename, quality=90):
    resaved_filename = 'tempresaved.jpg'
    im = Image.open(filename)
    bm = im.convert('RGB')
    im.close()
    im = bm
    im.save(resaved_filename, 'JPEG', quality=quality)
    resaved_im = Image.open(resaved_filename)
    ela_im = ImageChops.difference(im, resaved_im)
    extrema = ela_im.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)
    im.close()
    bm.close()
    resaved_im.close()
    return ela_im


def load_fake_detection_model():
    if os.path.exists(f"./cnn_model/{model_config.cnn_model_file_name}"):
        return keras.models.load_model(f"./cnn_model/{model_config.cnn_model_file_name}")
    return None
