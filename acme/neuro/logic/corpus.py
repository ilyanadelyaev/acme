# coding: utf-8
from __future__ import unicode_literals

import logging

import acme.neuro.logic.sentence as _sentence


logger = logging.getLogger(__name__)


def process_csv(
        file_path,
        dictionary,
):
    logger.info('Read "%s" corpus file', file_path)

    data = []

    word_id = len(dictionary)
    total_words_count = 0

    i = 0

    with open(file_path, 'rb') as f:
        for line in f:
            i += 1
            if i % 10000 == 0:
                logger.info('Processed %s items', i)

            # get sentence from csv

            line = line.decode('utf8')

            line = line.split(';')
            if len(line) < 4:
                continue
            line = line[3]

            line = line.strip('"')

            # prepare sentence

            sentence = _sentence.prepare(line)
            if not sentence:
                continue

            # encode

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
