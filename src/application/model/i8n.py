###
#
#   Full history: see below
#
#   Version: 1.0.0
#   Date: 2020-04-17
#   Author: Yves Vindevogel (vindevoy)
#
#
###

import logging
import os

from pathlib import Path

from common.content import Content
from common.singleton import Singleton
from common.options import Options


class I8N(metaclass=Singleton):
    __base_dir = 'i8n'
    __logger = None

    def __init__(self):
        self.__logger = logging.getLogger('MODEL.I8N')
        self.__logger.setLevel(Options().default_logging_level)

    @property
    def data(self):
        data = {}

        i8n_dir = os.path.join(Options().data_dir, self.__base_dir)

        for file in os.scandir(i8n_dir):
            stem = Path(file).stem
            self.__logger.debug('data - reading file {0}.yml'.format(stem))

            data[stem] = Content().load_data_yaml(self.__base_dir, file)

        self.__logger.debug('data - {0}'.format(data))

        return data
