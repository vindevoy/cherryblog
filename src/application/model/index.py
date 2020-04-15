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

import logging
import math
import os

from pathlib import Path

from common.content import Content
from common.options import Options
from common.singleton import Singleton

##
#   Do NOT import the DataLoader class, or you will have a circular reference, pass it through __init__ !!
##


class Index(metaclass=Singleton):
    __base_dir = 'index'
    __main_menu_settings_dir = 'main_menu'
    __footer_menu_settings_dir = 'footer_menu'

    __logger = None
    __data_loader = None

    __data = {}

    main_menu = None
    footer_menu = None

    max_posts = 0
    spotlight_posts = 0
    highlight_posts = 0

    def __init__(self, data_loader):
        self.__logger = logging.getLogger('MODEL.INDEX')
        self.__logger.setLevel(Options().default_logging_level)

        self.__data_loader = data_loader

        self.main_menu = Content().load_data_settings_yaml(self.__main_menu_settings_dir)
        self.__logger.debug('__init__ - main_menu: {0}'.format(self.main_menu))

        self.footer_menu = Content().load_data_settings_yaml(self.__footer_menu_settings_dir)
        self.__logger.debug('__init__ - footer_menu: {0}'.format(self.footer_menu))

        settings = Content().load_data_settings_yaml(self.__base_dir)
        self.__logger.debug('__init__ - settings: {0}'.format(settings))

        self.max_posts = settings['max_posts']
        self.spotlight_posts = settings['spotlight_posts']
        self.highlight_posts = settings['highlight_posts']

    def data(self, page_index):
        self.__logger.debug('data - page_index: {0}'.format(page_index))

        key_index = 'index-{0}'.format(page_index)

        if key_index in self.__data.keys():
            self.__logger.debug('data - index page found: {0}'.format(page_index))
            return self.__data[key_index]
        else:
            self.__logger.debug('data - index page not found: {0}'.format(page_index))

        data = self.__data_loader.common_data
        self.__logger.debug('data - common_data: {0}'.format(data))

        data_index = {}

        intro_meta, data_index['introduction'] = Content().read_content('index', 'introduction.md')

        data_index['image'] = intro_meta['image']

        data['index'] = data_index
        self.__logger.debug('data - data[index]: {0}'.format(data_index))

        posts_dir = os.path.join(Options().data_dir, 'posts')
        self.__logger.debug('data - posts_dir: {0}'.format(posts_dir))

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

        for file in sorted(os.listdir(posts_dir), reverse=True):
            count_entries += 1

            # We count the entries, but for pages 2 and more, you don't show them
            if skip_entries >= count_entries:
                continue

            post, post['content'] = Content().read_content(posts_dir, file)

            stem = Path(file).stem
            post['url'] = stem

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

        total_posts = self.__data_loader.posts_count
        total_index_pages = math.ceil(total_posts / max_entries)
        self.__logger.debug('data - total_posts: {0}'.format(total_posts))
        self.__logger.debug('data - total_index_pages: {0}'.format(total_index_pages))

        data['pagination'] = {'current_page': int(page_index),
                              'total_pages': total_index_pages,
                              'spotlight_posts': len(data['spotlight_posts']),
                              'highlight_posts': len(data['highlight_posts']),
                              'posts': len(data['posts'])}

        self.__data[key_index] = data
        self.__logger.debug('data - {0}'.format(data))

        return data
