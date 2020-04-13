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

import os
import math

from pathlib import Path

from common.content import Content
from common.options import Options
from common.singleton import Singleton

##
#   Do NOT import the DataLoader class, or you will have a circular reference, pass it through __init__ !!
##


class Index(metaclass=Singleton):
    __settings_dir = 'index'
    __main_menu_settings_dir = 'main_menu'
    __footer_menu_settings_dir = 'footer_menu'
    __data_loader = None

    main_menu = None
    footer_menu = None

    max_posts = 0
    spotlight_posts = 0
    highlight_posts = 0

    def __init__(self, data_loader):
        self.__data_loader = data_loader

        self.main_menu = Content().load_data_settings_yaml(self.__main_menu_settings_dir)
        self.footer_menu = Content().load_data_settings_yaml(self.__footer_menu_settings_dir)

        settings = Content().load_data_settings_yaml(self.__settings_dir)

        self.max_posts = settings['max_posts']
        self.spotlight_posts = settings['spotlight_posts']
        self.highlight_posts = settings['highlight_posts']

    # TODO: data must be kept in memory

    def data(self, page_index):
        data = self.__data_loader.common_data

        data_index = {}

        # TODO: this must be a method in content

        intro_dir = os.path.join(Options().data_dir, 'index')
        intro_file = open(os.path.join(intro_dir, 'introduction.md'), 'r')

        intro_meta, data_index['introduction'] = Content().split_file(intro_file.read())

        data_index['image'] = intro_meta['image']

        data['index'] = data_index

        posts_dir = os.path.join(Options().data_dir, 'posts')

        data['posts'] = []
        data['spotlight_posts'] = []
        data['highlight_posts'] = []

        # For now we take the list of files in reversed sort order
        # (newest should get a newer entry at the end of the list, like post1, ..., postx)
        # I will sort this out later

        max_entries = self.max_posts
        spotlight_entries = self.spotlight_posts
        highlight_entries = self.highlight_posts

        count_entries = 0
        skip_entries = (int(page_index) - 1) * max_entries

        for file in sorted(os.listdir(posts_dir), reverse=True):
            count_entries += 1

            # We count the entries, but for pages 2 and more, you don't show them
            if skip_entries >= count_entries:
                continue

            file = open(os.path.join(posts_dir, file), 'r')

            post, post['content'] = Content().split_file(file.read())

            stem = Path(file.name).stem
            post['url'] = stem

            if page_index == 1:
                if count_entries <= spotlight_entries:
                    data['spotlight_posts'].append(post)

                if spotlight_entries < count_entries <= (spotlight_entries + highlight_entries):
                    data['highlight_posts'].append(post)

                if count_entries > (spotlight_entries + highlight_entries):
                    data['posts'].append(post)

            else:
                data['posts'].append(post)

            if count_entries == (max_entries + skip_entries):
                break

        total_posts = self.__data_loader.posts_count
        total_index_pages = math.ceil(total_posts / max_entries)

        data['pagination'] = {'current_page': int(page_index),
                              'total_pages': total_index_pages,
                              'spotlight_posts': len(data['spotlight_posts']),
                              'highlight_posts': len(data['highlight_posts']),
                              'posts': len(data['posts'])}

        return data
