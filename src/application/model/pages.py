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
    __base_dir = 'pages'
    __data_loader = None

    __pages = {}

    directory = None
    count = 0

    def __init__(self, data_loader):
        self.__data_loader = data_loader

        self.directory = os.path.join(Options().data_dir, self.__base_dir)
        self.count = len(os.listdir(self.directory))

    def data(self, page):
        if page in self.__pages.keys():
            return self.__pages[page]

        data = self.__data_loader.common_data

        meta, content = Content().read_content(self.__base_dir, '{0}.md'.format(page))

        meta['content'] = content
        data['page'] = meta

        self.__pages[page] = data

        return data
