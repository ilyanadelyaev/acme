# coding: utf-8
from __future__ import unicode_literals

import re
import logging

import Stemmer


logger = logging.getLogger(__name__)


def prepare(file_path):
    logger.info('Read "%s" corpus file', file_path)

    raw_data = []

    i = 0

    stemmer = Stemmer.Stemmer('russian')  # pylint: disable=E1101

    with open(file_path, 'rb') as f:
        for line in f:

            line = line.decode('utf8')
            line = line.lower()

            i += 1
            if i % 10000 == 0:
                logger.info('Prepared %s items', i)

            if not line:
                continue

            # get sentence from csv

            sentence = line.split(';')
            if len(sentence) < 4:
                continue
            sentence = sentence[3]
            sentence = sentence.strip('"')

            # clear sentence. only words and numbers

            sentence = re.sub('[^#а-яa-z\s]*', '', sentence)
            sentence = re.sub(r'\s+', ' ', sentence)

            # make array

            sentence = sentence.split(' ')

            # prepare words with Stemmer

            sentence = stemmer.stemWords(sentence)

            #

            raw_data.append(sentence)

    logger.info('Corpus prepared. Amount %s items', len(raw_data))

    return raw_data


def encode_to_numbers(raw_data):
    logger.info('Encode %s items', len(raw_data))

    data = []

    dictionary = {}
    word_id = 0
    total_words_count = 0

    i = 0

    for sentence in raw_data:

        i += 1
        if i % 10000 == 0:
            logger.info('Encoded %s items', i)

        result = []

        for word in sentence:

            total_words_count += 1

            if word not in dictionary:
                dictionary[word] = word_id
                word_id += 1

            result.append(dictionary[word])

        data.append(result)

    logger.info(
        'Encoded %s items. Dictionary size: %s. Amount %s words encoded',
        len(data),
        len(dictionary),
        total_words_count,
    )

    return data, dictionary
