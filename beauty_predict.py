import os
import pickle
import sys

import cv2
import keras
import numpy as np
from keras.applications.resnet50 import ResNet50
from keras.layers import (Conv2D, Dense, Dropout, Flatten,
                          GlobalAveragePooling2D, Input, MaxPool2D, Permute)
from keras.models import Model, Sequential
from keras.optimizers import Adam, adam

import dlib
from config import output_path, parent_path

model_path = parent_path / "common" / "mmod_human_face_detector.dat"

cnn_face_detector = dlib.cnn_face_detection_model_v1(str(model_path))

resnet = ResNet50(include_top=False, pooling='avg')
model = Sequential()
model.add(resnet)
model.add(Dense(5, activation='softmax'))
model.layers[0].trainable = False

model.load_weights('model-ldl-resnet.h5')

def score_mapping(modelScore):

    if modelScore <= 1.9:
        mappingScore = ((4 - 2.5) / (1.9 - 1.0)) * (modelScore-1.0) + 2.5
    elif modelScore <= 2.8:
        mappingScore = ((5.5 - 4) / (2.8 - 1.9)) * (modelScore-1.9) + 4
    elif modelScore <= 3.4:
        mappingScore = ((6.5 - 5.5) / (3.4 - 2.8)) * (modelScore-2.8) + 5.5
    elif modelScore <= 4:
        mappingScore = ((8 - 6.5) / (4 - 3.4)) * (modelScore-3.4) + 6.5
    elif modelScore < 5:
        mappingScore = ((9 - 8) / (5 - 4)) * (modelScore-4) + 8

    return mappingScore


def predict_face(d, im):
    face = [d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom()]
    croped_im = im[face[1]:face[3], face[0]:face[2], :]
    resized_im = cv2.resize(croped_im, (224, 224))
    normed_im = np.array([(resized_im - 127.5) / 127.5])

    pred = model.predict(normed_im)
    ldList = pred[0]
    out = 1 * ldList[0] + 2 * ldList[1] + 3 * ldList[2] + 4 * ldList[3] + 5 * ldList[4]

    out = score_mapping(out)

    cv2.rectangle(im, (face[0], face[1]), (face[2], face[3]), (0, 255, 0), 3)
    cv2.putText(im, str('%.2f' % (out)), (face[0], face[3]), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2)

    return out


def beauty_predict(path, img):
    path = str(path / img)
    im0 = cv2.imread(path)

    if im0.shape[0] > 1280:
        new_shape = (1280, im0.shape[1] * 1280 / im0.shape[0])
    elif im0.shape[1] > 1280:
        new_shape = (im0.shape[0] * 1280 / im0.shape[1], 1280)
    elif im0.shape[0] < 640 or im0.shape[1] < 640:
        new_shape = (im0.shape[0] * 2, im0.shape[1] * 2)
    else:
        new_shape = im0.shape[0:2]

    im = cv2.resize(im0, (int(new_shape[1]), int(new_shape[0])))
    dets = cnn_face_detector(im, 0)

    # we expect only 1 face on a photo
    if len(dets) == 0:
        raise ValueError('No faces detected in image ' + path)
    elif len(dets) > 1:
        raise ValueError('More than 1 face detected in image ' + path)

    out = predict_face(dets[0], im)

    output_img = str(output_path / img)
    cv2.imwrite(output_img, im)

    return out
