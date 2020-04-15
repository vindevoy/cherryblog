###
#
#   Full history: see below
#
#   Version: 1.1.0
#   Date: 2020-04-15
#   Author: Yves Vindevogel (vindevoy)
#
#   Added logging
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


class Posts(metaclass=Singleton):
    __base_dir = 'posts'

    __logger = None
    __data_loader = None

    __posts = {}

    directory = None
    count = 0

    def __init__(self, data_loader):
        self.__logger = logging.getLogger('MODEL.POSTS')
        self.__logger.setLevel(Options().default_logging_level)

        self.__data_loader = data_loader

        self.directory = os.path.join(Options().data_dir, self.__base_dir)

        try:
            self.count = len(os.listdir(self.directory))
        except FileNotFoundError:
            self.count = 0

        self.__logger.debug('__init__ - directory: {0}'.format(self.directory))
        self.__logger.debug('__init__ - count: {0}'.format(self.count))

    def data(self, post):
        self.__logger.debug('data - post: {0}'.format(post))

        if post in self.__posts.keys():
            self.__logger.debug('data - post found: {0}'.format(post))
            return self.__posts[post]
        else:
            self.__logger.debug('data - post not found: {0}'.format(post))

        data = self.__data_loader.common_data
        self.__logger.debug('data - common_data: {0}'.format(data))

        meta, content = Content().read_content(self.__base_dir, '{0}.md'.format(post))

        meta['content'] = content
        data['post'] = meta

        self.__posts[post] = data
        self.__logger.debug('data - posts[{0}]: {1}'.format(post, data))

        return data


###
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
