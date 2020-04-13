###
#
#   Full history: see below
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

import os

from common.singleton import Singleton
from common.content import Content
from common.options import Options

##
#   Do NOT import the DataLoader class, or you will have a circular reference, pass it through __init__ !!
##


class Posts(metaclass=Singleton):
    __base_dir = 'posts'
    __data_loader = None

    __posts = {}

    directory = None
    count = 0

    def __init__(self, data_loader):
        self.__data_loader = data_loader

        self.directory = os.path.join(Options().data_dir, self.__base_dir)
        self.count = len(os.listdir(self.directory))

    def data(self, post):
        if post in self.__posts.keys():
            return self.__posts[post]

        data = self.__data_loader.common_data

        meta, content = Content().read_content(self.__base_dir, '{0}.md'.format(post))

        meta['content'] = content
        data['post'] = meta

        self.__posts[post] = data

        return data
