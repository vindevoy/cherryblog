###
#
#   Full history: see below
#
#   Version: 1.2.0
#   Date: 2020-04-17
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Caching done outside this class
#
###

import logging
import math
import os
import string

from operator import itemgetter
from pathlib import Path

from common.content import Content
from common.options import Options
from common.singleton import Singleton


class Tags(metaclass=Singleton):
    __base_dir = 'tags'

    __logger = None

    def __init__(self):
        self.__logger = logging.getLogger('MODEL.TAGS')
        self.__logger.setLevel(Options().default_logging_level)

    def list(self, posts_dir):
        self.__logger.debug('list - posts_dir: {0}'.format(posts_dir))

        settings = Content().load_data_settings_yaml(self.__base_dir)
        self.__logger.debug('list - settings: {0}'.format(settings))

        # Starting with a dictionary as this is the easiest to find existing tags
        tags = {}

        try:
            for file in os.listdir(posts_dir):
                meta, _, _ = Content().read_content(posts_dir, file)  # No need to catch the content

                for tag in meta['tags']:
                    label = self.__tag_label(tag)

                    if label in settings['skip_tags']:
                        self.__logger.debug('list - tag {0} found in skip_tags'.format(tag))
                        continue

                    if label in tags.keys():
                        self.__logger.debug('list - tag {0} already exists, +1'.format(tag))
                        current_count = tags[label]['count']
                        tags[label]['count'] = current_count + 1
                    else:
                        self.__logger.debug('list - tag {0} does not already exist'.format(tag))
                        data = {'label': label, 'count': 1, 'text': string.capwords(tag)}
                        tags[label] = data
        except FileNotFoundError:
            self.__logger.warning('COULD NOT FIND THE POSTS DIRECTORY {0}'.format(posts_dir))
            pass

        self.__logger.debug('list - tags: '.format(tags))

        # Pushing this into a simple array for Jinja2
        tags_array = []

        for _, value in tags.items():  # Only need the value
            tags_array.append(value)

        tags_list = sorted(tags_array, key=itemgetter('count'), reverse=True)
        self.__logger.debug('list - sorted tags: '.format(tags_list))

        return tags_list

    def data(self, posts_dir, tag, page_index, index_max_posts, count_tag_posts):
        self.__logger.debug('data - posts_dir: {0}'.format(posts_dir))
        self.__logger.debug('data - tag: {0}'.format(tag))
        self.__logger.debug('data - page_index tags: {0}'.format(page_index))
        self.__logger.debug('data - index_max_posts tags: {0}'.format(index_max_posts))
        self.__logger.debug('data - count_tag_posts tags: {0}'.format(count_tag_posts))

        data = {'posts': []}

        count_entries = 0
        max_entries = index_max_posts
        skip_entries = (int(page_index) - 1) * max_entries
        self.__logger.debug('data - max_entries: {0}'.format(max_entries))
        self.__logger.debug('data - skip_entries: {0}'.format(skip_entries))

        try:
            for file in sorted(os.listdir(posts_dir), reverse=True):
                post, _, post['content'] = Content().read_content(posts_dir, file)
                self.__logger.debug('data - post: {0}'.format(post))

                must_include = False

                for tag_raw in post['tags']:
                    if self.__tag_label(tag_raw) == tag:
                        must_include = True
                        break

                self.__logger.debug('data - must_include: {0}'.format(must_include))

                if must_include:
                    count_entries += 1

                    # We count the entries, but for pages 2 and more, you don't show them
                    if skip_entries >= count_entries:
                        self.__logger.debug('data - post skipped}')
                        continue
                    else:
                        self.__logger.debug('data - post added')

                    stem = Path(file).stem
                    post['url'] = stem

                    data['posts'].append(post)

                    if count_entries == max_entries:
                        self.__logger.debug('data - enough posts')
                        break
        except FileNotFoundError:
            pass

        data['tag'] = {'name': self.__tag_text(tag), 'path': tag}

        total_index_pages = math.ceil(count_tag_posts / max_entries)
        self.__logger.debug('data - total_index_pages: {0}'.format(total_index_pages))

        data['pagination'] = {'current_page': int(page_index), 'total_pages': total_index_pages}

        self.__logger.debug('data - {0}'.format(data))

        return data

    def count_posts(self, posts_dir, tag):
        self.__logger.debug('count_posts - tag: {0}'.format(tag))
        self.__logger.debug('count_posts - posts_dir: {0}'.format(posts_dir))

        count_entries = 0

        try:
            for file in os.listdir(posts_dir):
                post, _, _ = Content().read_content(posts_dir, file)

                for tag_raw in post['tags']:
                    if self.__tag_label(tag_raw) == tag:
                        count_entries += 1
                        self.__logger.debug('count_posts - file {0} includes tag '.format(file))
                        break
        except FileNotFoundError:
            pass

        self.__logger.debug('count_posts - tag {0} has {1} posts'.format(tag, count_entries))

        return count_entries

    @staticmethod
    def __tag_label(tag):
        return tag.lower().replace(' ', '-')

    @staticmethod
    def __tag_text(tag):
        return string.capwords(tag.replace('-', ' '))


###
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
