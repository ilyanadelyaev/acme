# coding: utf-8
from __future__ import unicode_literals

import re
import logging

import Stemmer


logger = logging.getLogger(__name__)


stemmer = Stemmer.Stemmer('russian')  # pylint: disable=E1101


def prepare(line):
    if not line:
        return

    sentence = line.lower()

    # clear sentence. only words and numbers

    sentence = re.sub('[^#а-яa-z\s]*', '', sentence)
    sentence = re.sub(r'\s+', ' ', sentence)

    # make array

    sentence = sentence.split(' ')

    # prepare words with Stemmer

    sentence = stemmer.stemWords(sentence)

    #

    return sentence
