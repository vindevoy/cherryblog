###
#
#   Full history: see below
#
#   Version: 1.1.0
#   Date: 2020-04-15
#   Author: Yves Vindevogel (vindevoy)
#
#   Added logging
#
###

import logging

from common.options import Options
from common.singleton import Singleton

##
#   Do NOT import the DataLoader class, or you will have a circular reference, pass it through __init__ !!
##


class CommonData(metaclass=Singleton):
    __logger = None
    __data_loader = None

    def __init__(self, data_loader):
        self.__logger = logging.getLogger('MODEL.COMMON_DATA')
        self.__logger.setLevel(Options().default_logging_level)

        self.__data_loader = data_loader

    def data(self):
        dl = self.__data_loader

        cd = {
                'settings': dl.global_settings,
                'tags_list': dl.tags_list,
                'tags_list_count': len(dl.tags_list),
                'main_menu': dl.index_main_menu,
                'footer_menu': dl.index_footer_menu,
                'important_news': dl.important_news_data,
                'code_version': dl.code_version_data
                }

        self.__logger.debug('data - {0}'.format(cd))

        return cd


###
#
#   Version: 1.0.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   This class was split of the DataLoader class
#
###
