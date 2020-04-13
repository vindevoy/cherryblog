###
#
#   Full history: see below
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
###

from common.singleton import Singleton
from model.codeversion import CodeVersion
from model.commondata import CommonData
from model.important_news import ImportantNews
from model.index import Index
from model.pages import Pages
from model.posts import Posts
from model.settings import Settings
from model.tags import Tags


class DataLoader(metaclass=Singleton):
    # code version
    @property
    def code_version_data(self):
        return CodeVersion().data

    # content
    @property
    def common_data(self):
        return CommonData(self).data()

    # important news
    @property
    def important_news_data(self):
        return ImportantNews().data

    # index
    @property
    def index_main_menu(self):
        return Index(self).main_menu

    @property
    def index_footer_menu(self):
        return Index(self).footer_menu

    def index_data(self, page_index):
        return Index(self).data(page_index)

    @property
    def index_max_posts(self):
        return Index(self).max_posts

    @property
    def index_spotlight_posts(self):
        return Index(self).spotlight_posts

    @property
    def index_highlight_posts(self):
        return Index(self).highlight_posts

    # pages
    @property
    def pages_count(self):
        return Pages(self).count

    def pages_data(self, page):
        return Pages(self).data(page)

    @property
    def pages_directory(self):
        return Pages(self).directory

    # posts
    @property
    def posts_count(self):
        return Posts(self).count

    def posts_data(self, post):
        return Posts(self).data(post)

    @property
    def posts_directory(self):
        return Posts(self).directory

    # settings
    @property
    def global_settings(self):
        return Settings().global_settings

    # tags
    def tags_posts_count(self, tag):
        return Tags(self).count_posts(tag)

    @property
    def tags_list(self):
        return Tags(self).list

    def tags_data(self, tag, page_index):
        return Tags(self).data(tag, page_index)

###
#
#   Version: 1.0.0
#   Date: 2020-04-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Original code
#
###
