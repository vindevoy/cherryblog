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

from common.content import Content
from common.singleton import Singleton


class ImportantNews(metaclass=Singleton):
    __settings_dir = 'important_news'

    data = None

    def __init__(self):
        self.data = Content().load_data_settings_yaml(self.__settings_dir)
