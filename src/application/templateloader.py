###
#
#   Version: 1.0.0
#   Date: 2020-03-29
#   Author: Yves Vindevogel (vindevoy)
#
###

import os

from jinja2 import Environment, FileSystemLoader

from settings import Settings
from singleton import Singleton


class TemplateLoader(metaclass=Singleton):
    __environment = None

    def __init__(self, template_root):
        self.__environment = Environment(loader=FileSystemLoader(os.path.join(Settings().root_dir, template_root)))

    def get_template(self, file):
        return self.__environment.get_template(file)
