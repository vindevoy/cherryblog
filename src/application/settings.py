###
#
#   Full history: see below
#
#   Version: 1.1.0
#   Date: 2020-04-09
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Uses a dynamic root directory where to retrieve the settings
#       - Dynamic paths to themes and data
#
###

import os
import yaml

from optionsloader import OptionsLoader
from singleton import Singleton


class Settings(metaclass=Singleton):
    __index_settings = None

    def __init__(self):
        settings_dir = os.path.join(OptionsLoader().data_dir, 'settings')
        file = open(os.path.join(settings_dir, 'index.yml'), 'r')

        self.__index_settings = yaml.load(file, Loader=yaml.SafeLoader)

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
#   Version: 1.0.1
#   Date: 2020-04-08
#   Author: Yves Vindevogel (vindevoy)
#
#   Fixes:
#       - Hard-coded values
#
#   Version: 1.0.0
#   Date: 2020-04-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Original code
#
###
