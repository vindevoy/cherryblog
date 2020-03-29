###
#
#   Version: 1.0.0
#   Date: 2020-03-29
#   Author: Yves Vindevogel (vindevoy)
#
###

import yaml
import os

from settings import Settings
from singleton import Singleton


class DataLoader(metaclass=Singleton):
    @staticmethod
    def get_data():
        data_dir = os.path.join(Settings().root_dir, 'src', 'data', 'site')
        file = open(os.path.join(data_dir, 'settings.yml'), 'r')

        data = yaml.load(file, Loader=yaml.SafeLoader)

        return data
