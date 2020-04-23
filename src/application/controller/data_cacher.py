
import logging

from common.options import Options
from common.singleton import Singleton


class DataCacher(metaclass=Singleton):
    __logger = None

    __cached_data = {}

    def __init__(self):
        self.__logger = logging.getLogger('DATA_CACHER')
        self.__logger.setLevel(Options().default_logging_level)

    def cached_already(self, key):
        return key in self.__cached_data.keys()

    def get_cached(self, key):
        return self.__cached_data[key]

    def cache(self, key, data):
        self.__logger.info('Caching {0}'.format(key))
        self.__cached_data[key] = data
