###
#
#   Full history: see below
#
#   Version: 1.1.0
#   Date: 2020-04-09
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Dynamic paths for data and theme
#
###

from jinja2 import Environment, FileSystemLoader

from optionsloader import OptionsLoader
from singleton import Singleton


class TemplateLoader(metaclass=Singleton):
    __environment = None

    def __init__(self):
        self.__environment = Environment(loader=FileSystemLoader(OptionsLoader().theme_dir))

    def get_template(self, file):
        return self.__environment.get_template(file)

###
#
#   Version: 1.0.0
#   Date: 2020-04-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Original code
#
###
