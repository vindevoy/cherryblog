###
#
#   Full history: see below
#
#   Version: 1.3.0
#   Date: 2020-05-01
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Removing skipped tags
#       - Rewrite date format
#
###

import logging
import os

from common.content import Content
from common.datetime_support import DateTimeSupport
from common.options import Options
from common.singleton import Singleton
from common.tags_support import TagsSupport


class Pages(metaclass=Singleton):
    __base_dir = 'pages'

    __logger = None

    def __init__(self):
        self.__logger = logging.getLogger('MODEL.PAGES')
        self.__logger.setLevel(Options().default_logging_level)

    @property
    def directory(self):
        directory = os.path.join(Options().data_dir, self.__base_dir)
        self.__logger.debug('directory - dir: {0}'.format(directory))

        return directory

    @property
    def files(self):
        directory = self.directory
        files = []

        for file in sorted(os.listdir(directory), reverse=False):
            entry = {'directory': self.__base_dir,
                     'file': file}

            files.append(entry)

        return files

    @property
    def count(self):
        try:
            count = len(os.listdir(self.directory))
        except FileNotFoundError:
            self.__logger.warning('COULD NOT FIND THE PAGES DIRECTORY {0}'.format(self.directory))
            count = 0

        self.__logger.debug('count - count: {0}'.format(count))

        return count

    def data(self, page, skip_tags):
        self.__logger.debug('data - page: {0}'.format(page))

        data = {}

        meta, content, html = Content().read_content(self.__base_dir, '{0}.md'.format(page))

        meta['content'] = html
        data['page'] = meta

        # remove the skipped tags
        tags = []

        try:
            for tag in data['page']['tags']:
                if TagsSupport().tag_label(tag) not in skip_tags:
                    tags.append(TagsSupport().tag_text(tag))
                else:
                    self.__logger.debug('data - removing skipped tag: {0}'.format(tag))
        except KeyError:
            pass

        data['page']['tags'] = tags
        self.__logger.debug('data - tags: {0}'.format(tags))

        data['page']['date'] = DateTimeSupport().rewrite_date(data['page']['date'])

        self.__logger.debug('data - pages[{0}]: {1}'.format(page, data))
        return data, meta, content


###
#
#   Version: 1.2.0
#   Date: 2020-04-17
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Caching done outside this class
#       - Added warning in Try Except
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
