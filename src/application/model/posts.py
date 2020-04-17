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
#       - Added warning on Try Except
#
###

import logging
import os

from common.content import Content
from common.options import Options
from common.singleton import Singleton


class Posts(metaclass=Singleton):
    __base_dir = 'posts'

    __logger = None

    def __init__(self):
        self.__logger = logging.getLogger('MODEL.POSTS')
        self.__logger.setLevel(Options().default_logging_level)

    @property
    def directory(self):
        directory = os.path.join(Options().data_dir, self.__base_dir)
        self.__logger.debug('directory - directory: {0}'.format(directory))

        return directory

    @property
    def count(self):
        try:
            count = len(os.listdir(self.directory))
        except FileNotFoundError:
            self.__logger.warning('COULD NOT FIND THE POSTS DIRECTORY {0}'.format(self.directory))
            count = 0

        self.__logger.debug('count - count: {0}'.format(count))

        return count

    def data(self, post):
        self.__logger.debug('data - post: {0}'.format(post))

        data = {}

        meta, content, html = Content().read_content(self.__base_dir, '{0}.md'.format(post))

        meta['content'] = html
        data['post'] = meta

        self.__logger.debug('data - posts[{0}]: {1}'.format(post, data))

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
#   Features:
#       - This class was split of the DataLoader class
#       - Data stored in memory
#
###
