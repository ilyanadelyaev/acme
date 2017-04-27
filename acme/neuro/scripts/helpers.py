# coding: utf-8
from __future__ import unicode_literals

import logging

import acme.tools.logger_setup as _logger


def setup_logging(level=None):
    if level is None:
        from acme.tools.config import config
        level = config['neuro/scripts/logger/level']

    _logger.setup_logging(
        level='DEBUG',
    )
