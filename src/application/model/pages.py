###
#
#   Full history: see below
#
#   Version: 1.0.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   This class was split of the DataLoader class
#
###

import logging
import os

from common.content import Content
from common.options import Options
from common.singleton import Singleton

##
#   Do NOT import the DataLoader class, or you will have a circular reference, pass it through __init__ !!
##


class Pages(metaclass=Singleton):
    __base_dir = 'pages'

    __logger = None
    __data_loader = None

    __pages = {}

    directory = None
    count = 0

    def __init__(self, data_loader):
        self.__logger = logging.getLogger('MODEL.PAGES')
        self.__logger.setLevel(Options().default_logging_level)

        self.__data_loader = data_loader

        self.directory = os.path.join(Options().data_dir, self.__base_dir)
        self.count = len(os.listdir(self.directory))
        self.__logger.debug('__init__ - directory: {0}'.format(self.directory))
        self.__logger.debug('__init__ - count: {0}'.format(self.count))

    def data(self, page):
        self.__logger.debug('data - page: {0}'.format(page))

        if page in self.__pages.keys():
            self.__logger.debug('data - page found: {0}'.format(page))
            return self.__pages[page]
        else:
            self.__logger.debug('data - page not found: {0}'.format(page))

        data = self.__data_loader.common_data
        self.__logger.debug('data - common_data: {0}'.format(data))

        meta, content = Content().read_content(self.__base_dir, '{0}.md'.format(page))

        meta['content'] = content
        data['page'] = meta

        self.__pages[page] = data
        self.__logger.debug('data - pages[{0}]: {1}'.format(page, data))

        return data
