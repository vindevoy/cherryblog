###
#
#   Version: 1.0.1
#   Date: 2020-04-08
#   Author: Yves Vindevogel (vindevoy)
#
#   Full history: see below
#
#   Fixes:
#       - Handcoded values
#
###

import os
import yaml

from singleton import Singleton


class Settings(metaclass=Singleton):
    __index_settings = None

    def __init__(self):
        settings_dir = os.path.join(self.root_dir, 'src', 'data', 'site')
        file = open(os.path.join(settings_dir, 'index.yml'), 'r')

        self.__index_settings = yaml.load(file, Loader=yaml.SafeLoader)

    @property
    def root_dir(self):
        return os.getcwd()

    @property
    def index_max_posts(self):
        return int(self.__index_settings['max_posts'])

    @property
    def index_spotlight_posts(self):
        return int(self.__index_settings['spotlight_posts'])

    @property
    def index_highlight_posts(self):
        return int(self.__index_settings['highlight_posts'])

###
#
#   Version: 1.0.0
#   Date: 2020-04-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Original file
#
###
