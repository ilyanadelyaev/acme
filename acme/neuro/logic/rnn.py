# coding: utf-8
from __future__ import unicode_literals

import logging

import numpy as np

import os
os.environ['KERAS_BACKEND'] = 'theano'

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM

import keras.models

from acme.tools.config import config

import acme.neuro.logic.sentence as _sentence


logger = logging.getLogger(__name__)


MAX_SENTENCE_LEN = 140  # words (because twitter)


def __prepare_x_y(
        dictionary,
        data,
):
    logger.debug('Prepare corpus. Amount %s items', len(data))

    x = np.zeros(
        (len(data), MAX_SENTENCE_LEN),
    )
    y = np.zeros(
        (len(data), 1),
    )
    for i, d in enumerate(data):
        x[i] = np.resize(d[0], (MAX_SENTENCE_LEN,))
        y[i] = d[1]

    split_at = int(len(x) * 0.9)
    x_train, x_test = x[:split_at], x[split_at:]
    y_train, y_test = y[:split_at], y[split_at:]

    logger.debug('Training Data: %s, %s', x_train.shape, y_train.shape)
    logger.debug('Test Data: %s, %s', x_test.shape, y_test.shape)

    return x_train, y_train, x_test, y_test


def train_model(
        dictionary,
        data,
):
    # prepare X Y

    x_train, y_train, x_test, y_test = __prepare_x_y(dictionary, data)

    # create model

    max_features = len(dictionary)

    model = Sequential()

    model.add(Embedding(max_features, 128, input_length=MAX_SENTENCE_LEN))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(64))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        # class_mode='binary',
    )

    # train model

    logger.debug(
        'Train model'
    )

    model.fit(
        x_train,
        y_train,
        batch_size=32,
        epochs=1,
    )

    logger.debug(
        'Model trained'
    )

    return model


def check_model(
        model,
        dictionary,
        data,
):
    # prepare X Y

    x_train, y_train, x_test, y_test = __prepare_x_y(dictionary, data)

    # validate

    scores = model.evaluate(x_test, y_test, verbose=0)

    logger.debug(
        'Model validation: %s / %s',
        model.metrics_names, scores,
    )


def load_model():
    with open(config['neuro/logic/model/json_path'], 'rb') as f:
        model = keras.models.model_from_json(f.read())
    model.load_weights(config['neuro/logic/model/h5_path'])
    return model


def predict(
        model,
        dictionary,
        sentences,
):
    data = []
    for s in sentences:
        s = _sentence.prepare(s)
        s = _sentence.encode(dictionary, s)
        data.append(s)

    x = np.zeros(
        (len(data), MAX_SENTENCE_LEN),
    )
    for i, d in enumerate(data):
        x[i] = np.resize(d, (MAX_SENTENCE_LEN,))

    result = model.predict_proba(x)

    return result
