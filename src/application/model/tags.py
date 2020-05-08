###
#
#   Full history: see below
#
#   Version: 1.4.0
#   Date: 2020-05-08
#   Author: Yves Vindevogel (vindevoy)
#
#   Changes:
#       - Support for drafts
#       - Remapping of URLs to documents
#
###

import logging
import math
import string

from operator import itemgetter
from pathlib import Path

from common.content import Content
from common.datetime_support import DateTimeSupport
from common.options import Options
from common.singleton import Singleton
from common.tags_support import TagsSupport
from controller.remapper import Remapper


class Tags(metaclass=Singleton):
    __base_dir = 'tags'

    __logger = None

    def __init__(self):
        self.__logger = logging.getLogger('MODEL.TAGS')
        self.__logger.setLevel(Options().default_logging_level)

    def skip_tags(self):
        settings = Content().load_data_settings_yaml(self.__base_dir)
        self.__logger.debug('list - settings: {0}'.format(settings))

        tags = []

        for tag in settings['skip_tags']:
            tags.append(TagsSupport().tag_label(tag))

        return tags

    def list(self, posts):
        self.__logger.debug('list - posts: {0}'.format(posts))

        settings = Content().load_data_settings_yaml(self.__base_dir)
        self.__logger.debug('list - settings: {0}'.format(settings))

        # Starting with a dictionary as this is the easiest to find existing tags
        tags = {}

        for entry in posts:
            directory = entry['directory']
            file = entry['file']

            meta, _, _ = Content().read_content(directory, file)  # No need to catch the content

            if meta['tags'] is None:
                continue

            for tag in meta['tags']:
                label = TagsSupport().tag_label(tag)

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

        self.__logger.debug('list - tags: '.format(tags))

        # Pushing this into a simple array for Jinja2
        tags_array = []

        for _, value in tags.items():  # Only need the value
            tags_array.append(value)

        for tag in tags_array:
            label = tag['label']
            unmapped = '/tags/{0}'.format(label)
            remapped = Remapper().remap_document(unmapped)

            if unmapped != remapped:
                label = remapped.split('/')[2]
                tag['label'] = label
                tag['text'] = TagsSupport().tag_text(label)

        tags_list = sorted(tags_array, key=itemgetter('count'), reverse=True)
        self.__logger.debug('list - sorted tags: '.format(tags_list))

        return tags_list

    def data(self, posts, tag, page_index, index_max_posts, count_tag_posts):
        self.__logger.debug('data - posts: {0}'.format(posts))
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

        for entry in posts:
            directory = entry['directory']
            file = entry['file']

            post, _, post['content'] = Content().read_content(directory, file)

            if post['tags'] is None:
                continue

            self.__logger.debug('data - post: {0}'.format(post))

            must_include = False

            for tag_raw in post['tags']:
                if TagsSupport().tag_label(tag_raw) == tag:
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
                url = '/posts/{0}'.format(stem)
                url = Remapper().remap_document(url)

                post['url'] = url
                post['date'] = DateTimeSupport().rewrite_date(post['date'])

                data['posts'].append(post)

                if count_entries == (max_entries + skip_entries):
                    self.__logger.debug('data - enough posts')
                    break

        data['tag'] = {'name': TagsSupport().tag_text(tag), 'path': tag}

        total_index_pages = math.ceil(count_tag_posts / max_entries)
        self.__logger.debug('data - total_index_pages: {0}'.format(total_index_pages))

        data['pagination'] = {'current_page': int(page_index), 'total_pages': total_index_pages}

        self.__logger.debug('data - {0}'.format(data))

        return data

    def count_posts(self, posts, tag):
        self.__logger.debug('count_posts - tag: {0}'.format(tag))
        self.__logger.debug('count_posts - posts: {0}'.format(posts))

        count_entries = 0

        for entry in posts:
            directory = entry['directory']
            file = entry['file']

            post, _, _ = Content().read_content(directory, file)

            if post['tags'] is None:
                continue

            for tag_raw in post['tags']:
                if TagsSupport().tag_label(tag_raw) == tag:
                    count_entries += 1
                    self.__logger.debug('count_posts - file {0} includes tag '.format(file))
                    break

        self.__logger.debug('count_posts - tag {0} has {1} posts'.format(tag, count_entries))

        return count_entries

###
#
#   Version: 1.3.0
#   Date: 2020-05-01
#   Author: Yves Vindevogel (vindevoy)
#
#   Changes:
#       - Moved the tag_label and tag_text methods to a support class in common
#       - Rewrite date format
#
#   Version: 1.2.1
#   Date: 2020-04-23
#   Author: Yves Vindevogel (vindevoy)
#
#   Fixes:
#       - Error on page with no tags
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
