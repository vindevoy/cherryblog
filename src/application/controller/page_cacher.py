###
#
#   Version: 1.0.0
#   Date: 2020-04-17
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       Simple page caching
#
###

import logging

from common.options import Options
from common.singleton import Singleton


class PageCacher(metaclass=Singleton):
    __logger = None

    __cached_pages = {}

    def __init__(self):
        self.__logger = logging.getLogger('PAGE_CACHER')
        self.__logger.setLevel(Options().default_logging_level)

    def cached_already(self, key):
        return key in self.__cached_pages.keys()

    def get_cached(self, key):
        return self.__cached_pages[key]

    def cache(self, key, data):
        self.__logger.info('Caching {0}'.format(key))
        self.__cached_pages[key] = data
