import os
os.environ['KERAS_BACKEND'] = 'theano'

from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM


model = None


def train_model(
        dictionary_size,
        positive_data,
        negative_data,
):
    global model

    max_features = dictionary_size
    maxlen = 100
    batch_size = 32

    model = Sequential()

    model.add(Embedding(max_features, 128, input_length=maxlen))
    model.add(LSTM(64, return_sequences=True))
    model.add(LSTM(64))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(
        loss='binary_crossentropy',
        optimizer='adam',
        class_mode='binary',
    )

    model.fit(
        positive_data,
        negative_data,
        batch_size=batch_size,
        nb_epoch=1,
        # show_accuracy=True,
    )


def predict(sentence):
    global model

    if model:
        return model.predict_proba(sentence)

    return None
