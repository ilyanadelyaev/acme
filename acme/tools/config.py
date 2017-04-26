import os
import sys
import logging
import argparse

import configure


logger = logging.getLogger(__name__)


class Config(object):
    """
    Usage:
    config = Config()
    print config['acme/proxy/https']
    """

    def __init__(self):
        try:
            self.__config = configure.Configuration.from_file(
                os.environ['CONFIG']
            ).configure()
        except (IOError, KeyError):
            self.__config = None
        #
        self._cache = {}

    def __getitem__(self, key):
        # get from cache
        value = self._cache.get(key, None)
        if value is not None:
            return value
        #
        if value is not None:
            value = value['Value']
            self._cache[key] = value
            return value
        # config
        value = self.__get_from_file_config(self.__config, key)
        if value is not None:
            self._cache[key] = value
            return value
        #
        raise KeyError('"{}" not exists'.format(key))

    def get(self, key, default_value=None):
        try:
            r_value = self.__getitem__(key)
        except KeyError:
            r_value = default_value
        return r_value

    @staticmethod
    def __get_from_file_config(source, key):
        if source is None:
            return None
        val = source
        for k in key.split('/'):
            try:
                val = val[k]
            except KeyError:
                return None
        return val


config = Config()
