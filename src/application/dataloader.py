###
#
#   Version: 1.0.0
#   Date: 2020-03-29
#   Author: Yves Vindevogel (vindevoy)
#
###

import markdown
import math
import yaml
import os
import string

from pathlib import Path
from operator import itemgetter

from settings import Settings
from singleton import Singleton


class DataLoader(metaclass=Singleton):
    @staticmethod
    def __get_settings():
        settings_dir = os.path.join(Settings().root_dir, 'src', 'data', 'site')
        file = open(os.path.join(settings_dir, 'settings.yml'), 'r')

        settings = yaml.load(file, Loader=yaml.SafeLoader)

        return settings

    def __get_categories(self):
        posts_dir = os.path.join(Settings().root_dir, 'src', 'data', 'posts')

        # Starting with a dictionary as this is the easiest to find existing categories
        categories = {}

        for file in os.listdir(posts_dir):
            file = open(os.path.join(posts_dir, file), 'r')

            meta, _ = self.__split_file(file.read())  # No need to catch the content

            for category in meta['categories']:
                label = self.__category_label(category)

                if label in categories.keys():
                    current_count = categories[label]['count']

                    categories[label]['count'] = current_count + 1
                else:
                    data = {'label': label, 'count': 1, 'text': string.capwords(category)}
                    categories[label] = data

        # Pushing this into a simple array for Jinja2
        categories_array = []

        for _, value in categories.items():  # Only need the value
            categories_array.append(value)

        return sorted(categories_array, key=itemgetter('count'), reverse=True)

    @staticmethod
    def __get_main_menu():
        config_dir = os.path.join(Settings().root_dir, 'src', 'data', 'site')
        file = open(os.path.join(config_dir, 'main_menu.yml'), 'r')

        menu = yaml.load(file, Loader=yaml.SafeLoader)

        return menu

    def __get_common(self):
        return {'settings': self.__get_settings(),
                'categories': self.__get_categories(),
                'main_menu': self.__get_main_menu()}

    @staticmethod
    def __count_pages():
        pages_dir = os.path.join(Settings().root_dir, 'src', 'data', 'pages')

        return len(os.listdir(pages_dir))

    @staticmethod
    def __count_posts():
        posts_dir = os.path.join(Settings().root_dir, 'src', 'data', 'posts')

        return len(os.listdir(posts_dir))

    def __count_category_posts(self, category):
        posts_dir = os.path.join(Settings().root_dir, 'src', 'data', 'posts')

        count_entries = 0

        for file in os.listdir(posts_dir):
            file = open(os.path.join(posts_dir, file), 'r')

            post, _ = self.__split_file(file.read())

            for cat_raw in post['categories']:
                if self.__category_label(cat_raw) == category:
                    count_entries += 1

        return count_entries

    def get_index_data(self, page_index):
        data = self.__get_common()

        posts_dir = os.path.join(Settings().root_dir, 'src', 'data', 'posts')

        data['posts'] = []

        # For now we take the list of files in reversed sort order
        # (newest should get a newer entry at the end of the list, like post1, ..., postx)
        # I will sort this out later

        max_entries = Settings().index_max_posts
        count_entries = 0
        skip_entries = (int(page_index) - 1) * max_entries

        for file in sorted(os.listdir(posts_dir), reverse=True):
            count_entries += 1

            # We count the entries, but for pages 2 and more, you don't show them
            if skip_entries >= count_entries:
                continue

            file = open(os.path.join(posts_dir, file), 'r')

            post, post['content'] = self.__split_file(file.read())

            stem = Path(file.name).stem
            post['url'] = stem

            data['posts'].append(post)

            if count_entries == (max_entries + skip_entries):
                break

        total_posts = self.__count_posts()
        total_index_pages = math.ceil(total_posts / max_entries)

        data['pagination'] = {'current_page': int(page_index), 'total_pages': total_index_pages}

        return data

    def get_category_data(self, category, page_index):
        data = self.__get_common()

        posts_dir = os.path.join(Settings().root_dir, 'src', 'data', 'posts')

        data['posts'] = []

        max_entries = Settings().index_max_posts
        count_entries = 0
        skip_entries = (int(page_index) - 1) * max_entries

        for file in sorted(os.listdir(posts_dir), reverse=True):
            file = open(os.path.join(posts_dir, file), 'r')

            post, post['content'] = self.__split_file(file.read())

            must_include = False

            for cat_raw in post['categories']:
                if self.__category_label(cat_raw) == category:
                    must_include = True
                    break

            if must_include:
                count_entries += 1

                # We count the entries, but for pages 2 and more, you don't show them
                if skip_entries >= count_entries:
                    continue

                stem = Path(file.name).stem
                post['url'] = stem

                data['posts'].append(post)

                if count_entries == max_entries:
                    break

        data['category'] = {'name': string.capwords(category.replace('-', ' ')), 'path': category}

        total_posts = self.__count_category_posts(category)
        total_index_pages = math.ceil(total_posts / max_entries)

        data['pagination'] = {'current_page': int(page_index), 'total_pages': total_index_pages}

        return data

    def get_page_data(self, page):
        data = self.__get_common()

        pages_dir = os.path.join(Settings().root_dir, 'src', 'data', 'pages')
        file = open(os.path.join(pages_dir, '{0}.md'.format(page)), 'r')

        meta, content = self.__split_file(file.read())

        meta['content'] = content
        data['page'] = meta

        return data

    def get_post_data(self, post):
        data = self.__get_common()

        posts_dir = os.path.join(Settings().root_dir, 'src', 'data', 'posts')
        file = open(os.path.join(posts_dir, '{0}.md'.format(post)), 'r')

        meta, content = self.__split_file(file.read())

        meta['content'] = content
        data['post'] = meta

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

    @staticmethod
    def __category_label(category):
        return category.lower().replace(' ', '-')
