###
#
#   Version: 1.0.0
#   Date: 2020-03-29
#   Author: Yves Vindevogel (vindevoy)
#
###

import markdown
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

    @staticmethod
    def get_main_menu():
        config_dir = os.path.join(Settings().root_dir, 'src', 'data', 'site')
        file = open(os.path.join(config_dir, 'main_menu.yml'), 'r')

        menu = yaml.load(file, Loader=yaml.SafeLoader)

        return menu

    def get_index_data(self):
        data = {'settings': self.get_settings(), 'main_menu': self.get_main_menu()}

        posts_dir = os.path.join(Settings().root_dir, 'src', 'data', 'posts')

        data['posts'] = []

        # For now we take the list of files in reversed sort order
        # (newest should get a newer entry at the end of the list, like post1, ..., postx)
        # I will sort this out later

        max_entries = Settings().index_max_posts
        count_entries = 0

        for file in sorted(os.listdir(posts_dir), reverse=True):
            count_entries += 1

            file = open(os.path.join(posts_dir, file), 'r')

            post, post['content'] = self.__split_file(file.read())

            stem = Path(file.name).stem
            post['url'] = stem

            data['posts'].append(post)

            if count_entries == max_entries:
                break

        return data

    def get_page_data(self, page):
        data = {'settings': self.get_settings(), 'main_menu': self.get_main_menu()}

        pages_dir = os.path.join(Settings().root_dir, 'src', 'data', 'pages')
        file = open(os.path.join(pages_dir, '{0}.md'.format(page)), 'r')

        data['page'], data['page']['content'] = self.__split_file(file.read())

        return data

    def get_post_data(self, post):
        data = {'settings': self.get_settings(), 'main_menu': self.get_main_menu()}

        posts_dir = os.path.join(Settings().root_dir, 'src', 'data', 'posts')
        file = open(os.path.join(posts_dir, '{0}.md'.format(post)), 'r')

        data['post'], data['post']['content'] = self.__split_file(file.read())

        return data

    @staticmethod
    def __split_file(data):
        split = data.split('-' * 10)

        meta = split[0]
        content = ""

        if len(split) == 2:
            content = split[1]

        meta_data = yaml.load(meta, Loader=yaml.SafeLoader)
        content_html = markdown.markdown(content)

        return meta_data, content_html
