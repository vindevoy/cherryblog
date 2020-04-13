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
import yaml

from common.content import Content
from common.options import Options
from common.singleton import Singleton


class Settings(metaclass=Singleton):
    __base_dir = 'settings'

    global_settings = None

    def __init__(self):
        settings_dir = os.path.join(Options().data_dir, self.__base_dir)

        self.global_settings = Content().load_yaml(settings_dir, 'global.yml')
