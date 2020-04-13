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

import os

from common.singleton import Singleton
from common.content import Content
from common.options import Options

##
#   Do NOT import the DataLoader class, or you will have a circular reference, pass it through __init__ !!
##


class Pages(metaclass=Singleton):
    # TODO: rename to base dir

    __settings_dir = 'pages'
    __data_loader = None

    directory = None
    count = 0

    def __init__(self, data_loader):
        self.__data_loader = data_loader

        self.directory = os.path.join(Options().data_dir, self.__settings_dir)
        self.count = len(os.listdir(self.directory))

    # TODO: data must be kept in memory

    def data(self, page):
        data = self.__data_loader.common_data

        # TODO: must be from content, reading content
        file = open(os.path.join(self.directory, '{0}.md'.format(page)), 'r')

        meta, content = Content().split_file(file.read())

        meta['content'] = content
        data['page'] = meta

        return data
