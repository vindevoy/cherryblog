###
#
#   Full history: see below
#
#   Version: 1.4.0
#   Date: 2020-05-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Support for drafts
#
###

import logging
import math

from pathlib import Path

from common.content import Content
from common.datetime_support import DateTimeSupport
from common.options import Options
from common.singleton import Singleton


class Index(metaclass=Singleton):
    __base_dir = 'index'
    __main_menu_settings_dir = 'main_menu'
    __footer_menu_settings_dir = 'footer_menu'

    __logger = None
    __settings = None

    def __init__(self):
        self.__logger = logging.getLogger('MODEL.INDEX')
        self.__logger.setLevel(Options().default_logging_level)

    def __get_settings(self):
        if self.__settings is None:
            content = Content().load_data_settings_yaml(self.__base_dir)
            self.__logger.debug('__get_settings - content: {0}'.format(content))

            self.__settings = content

        return self.__settings

    @property
    def max_posts(self):
        settings = self.__get_settings()
        return settings['max_posts']

    @property
    def spotlight_posts(self):
        settings = self.__get_settings()
        return settings['spotlight_posts']

    @property
    def highlight_posts(self):
        settings = self.__get_settings()
        return settings['highlight_posts']

    @property
    def main_menu(self):
        content = Content().load_data_settings_yaml(self.__main_menu_settings_dir)
        self.__logger.debug('main_menu: {0}'.format(content))

        return content

    @property
    def footer_menu(self):
        content = Content().load_data_settings_yaml(self.__footer_menu_settings_dir)
        self.__logger.debug('footer_menu: {0}'.format(content))

        return content

    def data(self, page_index, published_posts):
        self.__logger.debug('data - page_index: {0}'.format(page_index))

        data = {}
        self.__logger.debug('data - common_data: {0}'.format(data))

        data_index = {}

        intro_meta, intro_content, data_index['introduction'] = Content().read_content(self.__base_dir,
                                                                                       'introduction.md')

        data_index['image'] = intro_meta['image']

        data['index'] = data_index
        self.__logger.debug('data - data[index]: {0}'.format(data_index))

        data['posts'] = []
        data['spotlight_posts'] = []
        data['highlight_posts'] = []

        # For now we take the list of files in reversed sort order
        # (newest should get a newer entry at the end of the list, like post1, ..., postx)
        # I will sort this out later

        max_entries = self.max_posts
        spotlight_entries = self.spotlight_posts
        highlight_entries = self.highlight_posts
        self.__logger.debug('data - max_entries: {0}'.format(max_entries))
        self.__logger.debug('data - spotlight_entries: {0}'.format(spotlight_entries))
        self.__logger.debug('data - highlight_entries: {0}'.format(highlight_entries))

        count_entries = 0
        skip_entries = (int(page_index) - 1) * max_entries
        self.__logger.debug('data - skip_entries: {0}'.format(skip_entries))

        for entry in published_posts:
            directory = entry['directory']
            file = entry['file']
            count_entries += 1

            # We count the entries, but for pages 2 and more, you don't show them
            if skip_entries >= count_entries:
                continue

            post, _, post['content'] = Content().read_content(directory, file)

            stem = Path(file).stem
            post['url'] = stem
            post['date'] = DateTimeSupport().rewrite_date(post['date'])

            self.__logger.debug('data - post: {0}'.format(post))

            if page_index == 1:
                if count_entries <= spotlight_entries:
                    self.__logger.debug('data - post added to spotlight_posts.')
                    data['spotlight_posts'].append(post)

                if spotlight_entries < count_entries <= (spotlight_entries + highlight_entries):
                    self.__logger.debug('data - post added to highlight_posts.')
                    data['highlight_posts'].append(post)

                if count_entries > (spotlight_entries + highlight_entries):
                    self.__logger.debug('data - post added to (standard) posts.')
                    data['posts'].append(post)

            else:
                self.__logger.debug('data - post added to (standard) posts.')
                data['posts'].append(post)

            if count_entries == (max_entries + skip_entries):
                self.__logger.debug('data - enough posts for this index page.')
                break

        total_posts = len(published_posts)
        total_index_pages = math.ceil(total_posts / max_entries)
        self.__logger.debug('data - total_posts: {0}'.format(total_posts))
        self.__logger.debug('data - total_index_pages: {0}'.format(total_index_pages))

        data['pagination'] = {'current_page': int(page_index),
                              'total_pages': total_index_pages,
                              'spotlight_posts': len(data['spotlight_posts']),
                              'highlight_posts': len(data['highlight_posts']),
                              'posts': len(data['posts'])}

        self.__logger.debug('data - {0}'.format(data))

        return data, intro_content


###
#
#   Version: 1.3.0
#   Date: 2020-05-01
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Rewrite date format
#
#   Version: 1.2.0
#   Date: 2020-04-17
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Caching done outside this class
#
#   Version: 1.1.0
#   Date: 2020-04-15
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Added logging
#
#   Version: 1.0.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   This class was split of the DataLoader class
#
###
