###
#
#   Full history: see below
#
#   Version: 1.1.0
#   Date: 2020-04-15
#   Author: Yves Vindevogel (vindevoy)
#
#   Changes:
#       - Added logging
#       - Added try except on read of the files in case they don't exist
#
###

import logging
import markdown
import os
import yaml

from common.options import Options
from common.singleton import Singleton


class Content(metaclass=Singleton):
    __logger = None
    __meta_content_separator = None

    def __init__(self):
        self.__logger = logging.getLogger('COMMON.CONTENT')
        self.__logger.setLevel(Options().default_logging_level)

    def load_data_settings_yaml(self, directory):
        self.__logger.debug('load_data_settings_yaml - '
                            'Loading settings.yml from data sub-directory {0}.'.format(directory))

        return self.load_settings_yaml(os.path.join(Options().data_dir, directory))

    def load_settings_yaml(self, directory):
        self.__logger.debug('load_settings_yaml - Loading settings.yml from directory {0}.'.format(directory))

        return self.load_yaml(directory, 'settings.yml')

    def load_data_yaml(self, directory, file):
        self.__logger.debug('load_data_yaml - Loading {0} from directory {1}.'.format(file, directory))

        return self.load_yaml(os.path.join(Options().data_dir, directory), file)

    def load_yaml(self, directory, file):
        self.__logger.debug('load_yaml - Loading {0} from directory {0}.'.format(file, directory))

        # If the file cannot be read (for instance when the user deleted the directory in data)
        # don't care, return blanks
        try:
            yaml_file = open(os.path.join(directory, file), 'r')
        except FileNotFoundError:
            self.__logger.warning('COULD NOT FIND THE YAML FILE {0}/{1}'.format(directory, file))
            return {}

        content = yaml.load(yaml_file, Loader=yaml.SafeLoader)

        # In case there's an empty file, yaml returns a None instead of a empty structure
        if content is None:
            content = {}

        self.__logger.debug('load_yaml - Content of yaml:\n{0}'.format(content))

        return content

    def read_content(self, directory, file):
        content_dir = os.path.join(Options().data_dir, directory)
        self.__logger.debug('read_content - Reading content file {0} from directory {0}.'.format(file, content_dir))

        try:
            content_file = open(os.path.join(content_dir, file), 'r')
        except FileNotFoundError:
            self.__logger.warning('COULD NOT FIND THE YAML FILE {0}/{1}'.format(directory, file))
            return {}, ''

        meta, raw, html = self.__split_file(content_file.read())
        # No logging, already logged

        return meta, raw, html

    def __split_file(self, data):
        if self.__meta_content_separator is None:
            self.__meta_content_separator = Options().meta_content_separator

        self.__logger.debug('__split_file - Split file separator is {0}'.format(self.__meta_content_separator))

        split = data.split(self.__meta_content_separator)

        meta = split[0]
        content_raw = ""

        if len(split) == 2:
            content_raw = split[1]
        else:
            self.__logger.debug('__split_file - No content found.')

        meta_data = yaml.load(meta, Loader=yaml.SafeLoader)
        self.__logger.debug('__split_file - Meta data:\n{0}'.format(meta_data))

        self.__logger.debug('__split_file - Markdown data:\n{0}'.format(content_raw))
        content_html = markdown.markdown(content_raw)
        self.__logger.debug('__split_file - HTML:\n{0}'.format(content_html))

        return meta_data, content_raw, content_html

###
#
#   Version: 1.0.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   This class was split of the DataLoader class
#
###
