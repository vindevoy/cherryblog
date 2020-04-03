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
    def get_settings():
        settings_dir = os.path.join(Settings().root_dir, 'src', 'data', 'site')
        file = open(os.path.join(settings_dir, 'settings.yml'), 'r')

        settings = yaml.load(file, Loader=yaml.SafeLoader)

        return settings

    def get_index_data(self):
        data = {'blog': self.get_settings()}

        return data

    def get_page_data(self, page):
        data = {}

        pages_dir = os.path.join(Settings().root_dir, 'src', 'data', 'pages')
        file = open(os.path.join(pages_dir, '{0}.yml'.format(page)), 'r')

        page_data = yaml.load(file, Loader=yaml.SafeLoader)

        data['blog'] = self.get_settings()
        data['page'] = page_data

        return data

    def get_post_data(self):
        data = {'blog': self.get_settings()}

        return data
