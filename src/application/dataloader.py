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

import markdown
import math
import yaml
import os
import string

from pathlib import Path
from operator import itemgetter

from optionsloader import OptionsLoader
from settings import Settings
from singleton import Singleton


class DataLoader(metaclass=Singleton):
    @staticmethod
    def __get_settings():
        settings_dir = os.path.join(OptionsLoader().data_dir, 'settings')
        file = open(os.path.join(settings_dir, 'global.yml'), 'r')

        settings = yaml.load(file, Loader=yaml.SafeLoader)

        return settings

    def __get_tags(self):
        settings_dir = os.path.join(OptionsLoader().data_dir, 'tags_widget')
        file = open(os.path.join(settings_dir, 'settings.yml'), 'r')

        settings = yaml.load(file, Loader=yaml.SafeLoader)

        posts_dir = os.path.join(OptionsLoader().data_dir, 'posts')

        # Starting with a dictionary as this is the easiest to find existing tags
        tags = {}

        for file in os.listdir(posts_dir):
            file = open(os.path.join(posts_dir, file), 'r')

            meta, _ = self.__split_file(file.read())  # No need to catch the content

            for tag in meta['tags']:
                label = self.__tag_label(tag)

                if label in settings['skip_tags']:
                    continue

                if label in tags.keys():
                    current_count = tags[label]['count']

                    tags[label]['count'] = current_count + 1
                else:
                    data = {'label': label, 'count': 1, 'text': string.capwords(tag)}
                    tags[label] = data

        # Pushing this into a simple array for Jinja2
        tags_array = []

        for _, value in tags.items():  # Only need the value
            tags_array.append(value)

        return sorted(tags_array, key=itemgetter('count'), reverse=True)

    @staticmethod
    def __get_main_menu():
        config_dir = os.path.join(OptionsLoader().data_dir, 'main_menu')
        file = open(os.path.join(config_dir, 'settings.yml'), 'r')

        menu = yaml.load(file, Loader=yaml.SafeLoader)

        return menu

    @staticmethod
    def __get_footer_menu():
        config_dir = os.path.join(OptionsLoader().data_dir, 'footer_menu')
        file = open(os.path.join(config_dir, 'settings.yml'), 'r')

        menu = yaml.load(file, Loader=yaml.SafeLoader)

        return menu

    @staticmethod
    def __get_important_news():
        config_dir = os.path.join(OptionsLoader().data_dir, 'important_news_widget')
        file = open(os.path.join(config_dir, 'settings.yml'), 'r')

        news = yaml.load(file, Loader=yaml.SafeLoader)

        return news

    @staticmethod
    def __get_version():
        config_dir = os.path.join(OptionsLoader().data_dir, 'version_widget')
        file = open(os.path.join(config_dir, 'settings.yml'), 'r')

        versions = yaml.load(file, Loader=yaml.SafeLoader)

        return versions

    def __get_common(self):
        return {'settings': self.__get_settings(),
                'tags': self.__get_tags(),
                'main_menu': self.__get_main_menu(),
                'footer_menu': self.__get_footer_menu(),
                'important_news': self.__get_important_news(),
                'version': self.__get_version()
                }

    @staticmethod
    def __count_pages():
        pages_dir = os.path.join(OptionsLoader().data_dir, 'pages')

        return len(os.listdir(pages_dir))

    @staticmethod
    def __count_posts():
        posts_dir = os.path.join(OptionsLoader().data_dir, 'posts')

        return len(os.listdir(posts_dir))

    def __count_tag_posts(self, tag):
        posts_dir = os.path.join(OptionsLoader().data_dir, 'posts')

        count_entries = 0

        for file in os.listdir(posts_dir):
            file = open(os.path.join(posts_dir, file), 'r')

            post, _ = self.__split_file(file.read())

            for tag_raw in post['tags']:
                if self.__tag_label(tag_raw) == tag:
                    count_entries += 1

        return count_entries

    def get_index_data(self, page_index):
        data = self.__get_common()

        data_index = {}

        intro_dir = os.path.join(OptionsLoader().data_dir, 'index')
        intro_file = open(os.path.join(intro_dir, 'introduction.md'), 'r')

        intro_meta, data_index['introduction'] = self.__split_file(intro_file.read())

        data_index['image'] = intro_meta['image']

        data['index'] = data_index

        posts_dir = os.path.join(OptionsLoader().data_dir, 'posts')

        data['posts'] = []
        data['spotlight_posts'] = []
        data['highlight_posts'] = []

        # For now we take the list of files in reversed sort order
        # (newest should get a newer entry at the end of the list, like post1, ..., postx)
        # I will sort this out later

        max_entries = Settings().index_max_posts
        spotlight_entries = Settings().index_spotlight_posts
        highlight_entries = Settings().index_highlight_posts

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

        total_posts = self.__count_posts()
        total_index_pages = math.ceil(total_posts / max_entries)

        data['pagination'] = {'current_page': int(page_index),
                              'total_pages': total_index_pages,
                              'spotlight_posts': len(data['spotlight_posts']),
                              'highlight_posts': len(data['highlight_posts']),
                              'posts': len(data['posts'])}

        return data

    def get_tag_data(self, tag, page_index):
        data = self.__get_common()

        posts_dir = os.path.join(OptionsLoader().data_dir, 'posts')

        data['posts'] = []

        max_entries = Settings().index_max_posts
        count_entries = 0
        skip_entries = (int(page_index) - 1) * max_entries

        for file in sorted(os.listdir(posts_dir), reverse=True):
            file = open(os.path.join(posts_dir, file), 'r')

            post, post['content'] = self.__split_file(file.read())

            must_include = False

            for tag_raw in post['tags']:
                if self.__tag_label(tag_raw) == tag:
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

        data['tag'] = {'name': string.capwords(tag.replace('-', ' ')), 'path': tag}

        total_posts = self.__count_tag_posts(tag)
        total_index_pages = math.ceil(total_posts / max_entries)

        data['pagination'] = {'current_page': int(page_index), 'total_pages': total_index_pages}

        return data

    def get_page_data(self, page):
        data = self.__get_common()

        pages_dir = os.path.join(OptionsLoader().data_dir, 'pages')
        file = open(os.path.join(pages_dir, '{0}.md'.format(page)), 'r')

        meta, content = self.__split_file(file.read())

        meta['content'] = content
        data['page'] = meta

        return data

    def get_post_data(self, post):
        data = self.__get_common()

        posts_dir = os.path.join(OptionsLoader().data_dir, 'posts')
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
    def __tag_label(tag):
        return tag.lower().replace(' ', '-')

###
#
#   Version: 1.0.0
#   Date: 2020-04-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Original code
#
###
