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

import math
import os
import string

from operator import itemgetter
from pathlib import Path

from common.content import Content
from common.options import Options
from common.singleton import Singleton


class Tags(metaclass=Singleton):
    __settings_dir = 'tags'
    __data_loader = None

    list = None

    def __init__(self, data_loader):
        self.__data_loader = data_loader
        self.__build_list()

    def __build_list(self):
        settings_dir = os.path.join(Options().data_dir, self.__settings_dir)
        settings = Content().load_data_settings_yaml(settings_dir)

        posts_dir = self.__data_loader.posts_directory

        # Starting with a dictionary as this is the easiest to find existing tags
        tags = {}

        for file in os.listdir(posts_dir):
            file = open(os.path.join(posts_dir, file), 'r')

            meta, _ = Content().split_file(file.read())  # No need to catch the content

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

        self.list = sorted(tags_array, key=itemgetter('count'), reverse=True)

    def data(self, tag, page_index):
        data = self.__data_loader.common_data

        posts_dir = self.__data_loader.posts_directory

        data['posts'] = []

        max_entries = self.__data_loader.index_max_posts
        count_entries = 0
        skip_entries = (int(page_index) - 1) * max_entries

        for file in sorted(os.listdir(posts_dir), reverse=True):
            file = open(os.path.join(posts_dir, file), 'r')

            post, post['content'] = Content().split_file(file.read())

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

        data['tag'] = {'name': self.__tag_text(tag), 'path': tag}

        total_posts = self.count_posts(tag)
        total_index_pages = math.ceil(total_posts / max_entries)

        data['pagination'] = {'current_page': int(page_index), 'total_pages': total_index_pages}

        return data

    def count_posts(self, tag):
        posts_dir = self.__data_loader.posts_directory

        count_entries = 0

        for file in os.listdir(posts_dir):
            file = open(os.path.join(posts_dir, file), 'r')

            post, _ = Content().split_file(file.read())

            for tag_raw in post['tags']:
                if self.__tag_label(tag_raw) == tag:
                    count_entries += 1

        return count_entries

    @staticmethod
    def __tag_label(tag):
        return tag.lower().replace(' ', '-')

    @staticmethod
    def __tag_text(tag):
        return string.capwords(tag.replace('-', ' '))
