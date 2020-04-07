###
#
#   Version: 1.0.0
#   Date: 2020-03-29
#   Author: Yves Vindevogel (vindevoy)
#
###

import os

from singleton import Singleton


class Settings(metaclass=Singleton):
    @property
    def root_dir(self):
        return os.getcwd()

    @property
    def index_max_posts(self):
        return 4

    @property
    def index_spotlight_posts(self):
        return 1

    @property
    def index_highlight_posts(self):
        return 2
