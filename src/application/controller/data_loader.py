###
#
#   Full history: see below
#
#   Version: 1.3.0
#   Date: 2020-04-26
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Caching enabled or not
#
###

import logging

from common.options import Options
from common.singleton import Singleton
from controller.data_cacher import DataCacher
from model.codeversion import CodeVersion
from model.i8n import I8N
from model.important_news import ImportantNews
from model.index import Index
from model.pages import Pages
from model.posts import Posts
from model.search import Search
from model.settings import Settings
from model.tags import Tags


class DataLoader(metaclass=Singleton):
    __logger = None

    __cached_data = {}

    def __init__(self):
        self.__logger = logging.getLogger('DATA_LOADER')
        self.__logger.setLevel(Options().default_logging_level)

    @staticmethod
    def __get_data(key, cls, method):
        if Options().caching and DataCacher().cached_already(key):
            return DataCacher().get_cached(key)

        data = getattr(cls, method)

        if Options().caching:
            DataCacher().cache(key, data)

        return data

    @staticmethod
    def __combine(*parts):
        combined = {}

        for part in parts:
            for item in part.items():
                combined[item[0]] = item[1]

        return combined

    # code version
    @property
    def code_version_data(self):
        return self.__get_data('code_version_data', CodeVersion(), 'data')

    @property
    def common_data(self):
        key = 'common_data'

        if Options().caching and DataCacher().cached_already(key):
            return DataCacher().get_cached(key)

        data = {
                'i8n': self.i8n,
                'settings': self.global_settings,
                'tags_list': self.tags_list,
                'tags_list_count': self.tags_list_count,
                'main_menu': self.index_main_menu,
                'footer_menu': self.index_footer_menu,
                'important_news': self.important_news_data,
                'code_version': self.code_version_data
                }

        if Options().caching:
            DataCacher().cache(key, data)

        return data

    # important news
    @property
    def important_news_data(self):
        return self.__get_data('important_news_data', ImportantNews(), 'data')

    # i8n
    @property
    def i8n(self):
        return I8N().data

    # index
    @property
    def index_main_menu(self):
        return self.__get_data('index_main_menu', Index(), 'main_menu')

    @property
    def index_footer_menu(self):
        return self.__get_data('index_footer_menu', Index(), 'footer_menu')

    def index_data(self, page_index):
        key = '/index/{0}'.format(page_index)

        if Options().caching and DataCacher().cached_already(key):
            return DataCacher().get_cached(key)

        common = self.common_data
        data, _ = Index().data(page_index, self.posts_directory, self.posts_count)

        #  We don't care yet about the raw intro
        combined = self.__combine(common, data)

        if Options().caching:
            DataCacher().cache(key, combined)

        return combined

    @property
    def index_max_posts(self):
        return self.__get_data('index_max_posts', Index(), 'max_posts')

    @property
    def index_spotlight_posts(self):
        return self.__get_data('index_spotlight_posts', Index(), 'spotlight_posts')

    @property
    def index_highlight_posts(self):
        return self.__get_data('index_highlight_posts', Index(), 'highlight_posts')

    # pages
    @property
    def pages_directory(self):
        return self.__get_data('pages_directory', Pages(), 'directory')

    @property
    def pages_files(self):
        return self.__get_data('pages_files', Pages(), 'files')

    @property
    def pages_count(self):
        return self.__get_data('pages_count', Pages(), 'count')

    def pages_data(self, page):
        key = '/pages/{0}'.format(page)

        if Options().caching and DataCacher().cached_already(key):
            return DataCacher().get_cached(key)

        common = self.common_data
        data, _, _ = Pages().data(page)  # No catching the meta and raw data yet
        combined = self.__combine(common, data)

        if Options().caching:
            DataCacher().cache(key, combined)

        return combined

    # posts
    @property
    def posts_directory(self):
        return self.__get_data('posts_directory', Posts(), 'directory')

    @property
    def posts_files(self):
        return self.__get_data('posts_files', Posts(), 'files')

    @property
    def posts_count(self):
        return self.__get_data('posts_count', Posts(), 'count')

    def posts_data(self, post):
        key = '/posts/{0}'.format(post)

        if Options().caching and DataCacher().cached_already(key):
            return DataCacher().get_cached(key)

        common = self.common_data
        data, _, _ = Posts().data(post)  # We don't do anything with the meta and raw data yet
        combined = self.__combine(common, data)

        if Options().caching:
            DataCacher().cache(key, combined)

        return combined

    # search
    def search_data(self, query, page_index):
        search_base = []

        for page in self.pages_files:
            search_base.append(page)

        for post in self.posts_files:
            search_base.append(post)

        common = self.common_data
        data = Search().data(query, page_index, search_base, self.index_max_posts)
        combined = self.__combine(common, data)

        return combined

    # settings
    @property
    def global_settings(self):
        return self.__get_data('global_settings', Settings(), 'data')

    # tags
    def tags_posts_count(self, tag):
        key = 'tags_posts_count/{0}'.format(tag)

        if Options().caching and DataCacher().cached_already(key):
            return DataCacher().get_cached(key)

        data = Tags().count_posts(self.posts_directory, tag)

        if Options().caching:
            DataCacher().cache(key, data)

        return data

    @property
    def tags_list(self):
        key = 'tags_list'

        if Options().caching and DataCacher().cached_already(key):
            return DataCacher().get_cached(key)

        tags_list = Tags().list(self.posts_directory)

        if Options().caching:
            DataCacher().cache(key, tags_list)

        return tags_list

    @property
    def tags_list_count(self):
        return len(self.tags_list)

    def tags_data(self, tag, page_index):
        key = 'tags_data/{0}/{1}'.format(tag, page_index)

        if Options().caching and DataCacher().cached_already(key):
            return DataCacher().get_cached(key)

        common = self.common_data
        data = Tags().data(self.posts_directory, tag, page_index, self.index_max_posts, self.tags_posts_count(tag))
        combined = self.__combine(common, data)

        if Options().caching:
            DataCacher().cache(key, combined)

        return combined

###
#
#   Version: 1.2.0
#   Date: 2020-04-17
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Caching implemented in this class instead of model classes
#
#   Version: 1.1.0
#   Date: 2020-04-09
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Renaming categories to tags
#       - Added introduction to the index page
#       - Dynamic paths to themes and data
#       - Updated the path of the main menu settings file
#       - Data for important_news and version widget
#       - Data for footer_menu
#
#   Version: 1.0.0
#   Date: 2020-04-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Original code
#
###
