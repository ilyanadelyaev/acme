# coding: utf-8
from __future__ import unicode_literals

import json
import logging

from acme.tools.config import config

import acme.neuro.logic.sentence as _sentence


logger = logging.getLogger(__name__)


def __convert_value(value):
    if value == '0':
        return 0.5
    elif value == '-1':
        return 0.0
    elif value == '1':
        return 1.0
    else:
        return


def process_csv(
        file_path,
        dictionary,
        data,
):
    logger.info('Read "%s" corpus file', file_path)

    i = 0

    with open(file_path, 'rb') as f:
        for line in f:
            i += 1
            if i % 10000 == 0:
                logger.info('Processed %s items', i)

            # get sentence from csv

            line = line.decode('utf8')

            line = line.split('";"')
            if len(line) < 5:
                continue
            sentence = line[3]
            value = line[4]

            # prepare sentence

            sentence = _sentence.prepare(sentence)
            if not sentence:
                continue

            # encode

            sentence = _sentence.encode(dictionary, sentence, append_dict=True)

            # convert value

            value = __convert_value(value)
            if value is None:
                continue

            #

            data.append((
                sentence,
                value,
            ))

    logger.info(
        'Encoded %s items. Dictionary size: %s',
        len(data),
        len(dictionary),
    )

    return dictionary, data


def load_dictionary():
    with open(config['neuro/logic/corpus/json_path'], 'rb') as f:
        raw_data = json.loads(f.read())
    return raw_data['dictionary']
