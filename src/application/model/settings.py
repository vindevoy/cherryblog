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


class Settings(metaclass=Singleton):
    __base_dir = 'settings'
    __logger = None

    global_settings = None

    def __init__(self):
        self.__logger = logging.getLogger('MODEL.SETTINGS')
        self.__logger.setLevel(Options().default_logging_level)

        settings_dir = os.path.join(Options().data_dir, self.__base_dir)
        self.__logger.debug('__init__ - settings_dir: {0}'.format(settings_dir))

        self.global_settings = Content().load_yaml(settings_dir, 'global.yml')
        self.__logger.debug('__init__ - global_settings: {0}'.format(self.global_settings))

###
#
#   Version: 1.0.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   This class was split of the DataLoader class
#
###

