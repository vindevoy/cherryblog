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

from common.singleton import Singleton

##
#   Do NOT import the DataLoader class, or you will have a circular reference, pass it through __init__ !!
##


class CommonData(metaclass=Singleton):
    __data_loader = None

    def __init__(self, data_loader):
        self.__data_loader = data_loader

    def data(self):
        dl = self.__data_loader

        return {
                'settings': dl.global_settings,
                'tags_list': dl.tags_list,
                'main_menu': dl.index_main_menu,
                'footer_menu': dl.index_footer_menu,
                'important_news': dl.important_news_data,
                'code_version': dl.code_version_data
                }
