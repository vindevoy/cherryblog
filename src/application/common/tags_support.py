###
#
#   Full history: see below
#
#   Version: 1.0.0
#   Date: 2020-05-01
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Moved the function to this class because it's shared over other model classes
#
###

import logging
import string

from common.options import Options
from common.singleton import Singleton


class TagsSupport(metaclass=Singleton):
    __logger = None

    def __init__(self):
        self.__logger = logging.getLogger('COMMON.TAGS_SUPPORT')
        self.__logger.setLevel(Options().default_logging_level)

    @staticmethod
    def tag_label(tag):
        return tag.lower().replace(' ', '-')

    @staticmethod
    def tag_text(tag):
        return string.capwords(tag.replace('-', ' '))
