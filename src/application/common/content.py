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

import markdown
import os
import yaml

from common.options import Options
from common.singleton import Singleton


class Content(metaclass=Singleton):
    def load_data_settings_yaml(self, directory):
        return self.load_settings_yaml(os.path.join(Options().data_dir, directory))

    def load_settings_yaml(self, directory):
        return self.load_yaml(directory, 'settings.yml')

    @staticmethod
    def load_yaml(directory, file):
        yaml_file = open(os.path.join(directory, file), 'r')

        return yaml.load(yaml_file, Loader=yaml.SafeLoader)

    def read_content(self, directory, file):
        content_dir = os.path.join(Options().data_dir, directory)
        content_file = open(os.path.join(content_dir, file), 'r')

        meta, html = self.__split_file(content_file.read())

        return meta, html

    @staticmethod
    def __split_file(data):
        split = data.split('-' * 10)

        meta = split[0]
        content = ""

        if len(split) == 2:
            content = split[1]

        meta_data = yaml.load(meta, Loader=yaml.SafeLoader)
        content_html = markdown.markdown(content)

        return meta_data, content_html
