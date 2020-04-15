###
#
#   Full history: see below
#
#   Version: 1.2.0
#   Date: 2020-04-15
#   Author: Yves Vindevogel (vindevoy)
#
#   Added logging
#
###

import logging

from jinja2 import Environment, FileSystemLoader

from common.options import Options
from common.singleton import Singleton


class TemplateLoader(metaclass=Singleton):
    __logger = None
    __environment = None

    def __init__(self):
        self.__logger = logging.getLogger('VIEW.TEMPLATE_LOADER')
        self.__logger.setLevel(Options().default_logging_level)

        # Theme dir already logged in main
        self.__environment = Environment(loader=FileSystemLoader(Options().theme_dir))

    def get_template(self, file):
        self.__logger.debug('get_template - Template file {0}'.format(file))

        return self.__environment.get_template(file)

###
#
#   Version: 1.1.0
#   Date: 2020-04-09
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Dynamic paths for data and theme
#
#   Version: 1.0.0
#   Date: 2020-04-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Original code
#
###
