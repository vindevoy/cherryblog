###
#
#   Version: 1.0.0
#   Date: 2020-03-29
#   Author: Yves Vindevogel (vindevoy)
#
###

import yaml
import os

from pathlib import Path

from settings import Settings
from singleton import Singleton


class DataLoader(metaclass=Singleton):
    @staticmethod
    def get_settings():
        settings_dir = os.path.join(Settings().root_dir, 'src', 'data', 'site')
        file = open(os.path.join(settings_dir, 'settings.yml'), 'r')

        settings = yaml.load(file, Loader=yaml.SafeLoader)

        return settings

    def get_index_data(self):
        data = {'settings': self.get_settings()}

        posts_dir = os.path.join(Settings().root_dir, 'src', 'data', 'blog')

        data['posts'] = []

        # For now we take the list of files in reversed sort order
        # (newest should get a newer entry at the end of the list, like post1, ..., postx)
        # I will sort this out later

        max_entries = Settings().index_max_posts
        count_entries = 0

        for file in sorted(os.listdir(posts_dir), reverse=True):
            count_entries += 1

            file = open(os.path.join(posts_dir, file), 'r')
            post_data = yaml.load(file, Loader=yaml.SafeLoader)
            stem = Path(file.name).stem
            post_data['url'] = stem

            data['posts'].append(post_data)

            if count_entries == max_entries:
                break

        print (data)

        return data

    def get_page_data(self, page):
        data = {'settings': self.get_settings()}

        pages_dir = os.path.join(Settings().root_dir, 'src', 'data', 'pages')
        file = open(os.path.join(pages_dir, '{0}.yml'.format(page)), 'r')

        page_data = yaml.load(file, Loader=yaml.SafeLoader)

        data['page'] = page_data

        return data

    def get_post_data(self, post):
        data = {'settings': self.get_settings()}

        posts_dir = os.path.join(Settings().root_dir, 'src', 'data', 'blog')
        file = open(os.path.join(posts_dir, '{0}.yml'.format(post)), 'r')

        post_data = yaml.load(file, Loader=yaml.SafeLoader)

        data['post'] = post_data

        return data
