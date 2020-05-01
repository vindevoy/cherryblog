###
#
#   Full history: see below
#
#   Version: 1.0.0
#   Date: 2020-05-01
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Rewrite dates to nicer format
#
###

import logging
import datetime

from common.options import Options
from common.singleton import Singleton


class DateTimeSupport(metaclass=Singleton):
    __logger = None

    input_format = None
    output_format = None

    def __init__(self):
        self.__logger = logging.getLogger('COMMON.DATETIME_SUPPORT')
        self.__logger.setLevel(Options().default_logging_level)

    def rewrite_date(self, date):
        d = datetime.datetime.strptime(date, self.input_format)
        return d.strftime(self.output_format)

