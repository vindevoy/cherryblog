###
#
#   Full history: see below
#
#   Version: 1.2.0
#   Date: 2020-04-17
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Caching done outside this class
#       - Added warning in Try Except
#
###

import logging
import os

from common.content import Content
from common.options import Options
from common.singleton import Singleton


class Pages(metaclass=Singleton):
    __base_dir = 'pages'

    __logger = None

    def __init__(self):
        self.__logger = logging.getLogger('MODEL.PAGES')
        self.__logger.setLevel(Options().default_logging_level)

    @property
    def directory(self):
        directory = os.path.join(Options().data_dir, self.__base_dir)
        self.__logger.debug('directory - dir: {0}'.format(directory))

        return directory

    @property
    def count(self):
        try:
            count = len(os.listdir(self.directory))
        except FileNotFoundError:
            self.__logger.warning('COULD NOT FIND THE PAGES DIRECTORY {0}'.format(self.directory))
            count = 0

        self.__logger.debug('count - count: {0}'.format(count))

        return count

    def data(self, page):
        self.__logger.debug('data - page: {0}'.format(page))

        data = {}

        meta, content, html = Content().read_content(self.__base_dir, '{0}.md'.format(page))

        meta['content'] = html
        data['page'] = meta

        self.__logger.debug('data - pages[{0}]: {1}'.format(page, data))

        return data, meta, content


###
#
#   Version: 1.1.0
#   Date: 2020-04-15
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Added logging
#
#   Version: 1.0.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   This class was split of the DataLoader class
#
###