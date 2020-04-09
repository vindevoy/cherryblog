###
#
#   Version: 1.0.0
#   Date: 2020-04-09
#   Author: Yves Vindevogel (vindevoy)
#
###

from singleton import Singleton


class OptionsLoader(metaclass=Singleton):
    environment = ''
    data_dir = ''
    theme_dir = ''
