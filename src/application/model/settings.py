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

    def __init__(self):
        self.__logger = logging.getLogger('MODEL.SETTINGS')
        self.__logger.setLevel(Options().default_logging_level)

    @property
    def data(self):
        settings_dir = os.path.join(Options().data_dir, self.__base_dir)
        self.__logger.debug('data - settings_dir: {0}'.format(settings_dir))

        content = Content().load_yaml(settings_dir, 'global.yml')
        self.__logger.debug('data - content: {0}'.format(content))

        return content

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
