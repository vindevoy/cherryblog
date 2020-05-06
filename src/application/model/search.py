###
#
#   Full history: see below
#
#   Version: 1.1.1
#   Date: 2020-05-06
#   Author: Yves Vindevogel (vindevoy)
#
#   Fixes:
#       - The replace with the bold tags works, but it does not capture capital letters.  Introducing another method.
#
###

import logging

from pathlib import Path

from common.content import Content
from common.datetime_support import DateTimeSupport
from common.options import Options
from common.singleton import Singleton

from controller.data_cacher import DataCacher


class Search(metaclass=Singleton):
    __base_dir = 'search'

    __logger = None

    def __init__(self):
        self.__logger = logging.getLogger('MODEL.SEARCH')
        self.__logger.setLevel(Options().default_logging_level)

    def data(self, query, page_index, search_base, max_entries):
        self.__logger.debug('data - query: {0}'.format(query))
        self.__logger.debug('data - page_index: {0}'.format(page_index))
        self.__logger.debug('data - search_base: {0}'.format(search_base))

        settings = Content().load_data_settings_yaml(self.__base_dir)
        excluded = settings['excluded']

        self.__logger.debug('data - excluded: {0}'.format(excluded))

        data = {'found': []}

        page_index = int(page_index)
        count_entries = 0
        skip_entries = (page_index - 1) * max_entries
        first_entry = skip_entries + 1

        for item in search_base:
            self.__logger.debug('data - search_base item: {0}'.format(item))

            directory = item['directory']
            file = item['file']
            stem = Path(file).stem

            # adding the stem to the object for the final url
            item['stem'] = stem

            url = '/{0}/{1}'.format(directory, stem)

            if url in excluded:
                self.__logger.debug('data - excluded item: {0}'.format(item))
                continue

            cached_already = DataCacher().cached_already(url)

            if cached_already:
                self.__logger.debug('data - cached: {0}'.format(url))

                meta = DataCacher().get_cached('{0}/meta'.format(url))
                content = DataCacher().get_cached('{0}/content'.format(url))
            else:
                self.__logger.debug('data - not cached: {0}'.format(url))

                meta, content, _ = Content().read_content(directory, file)

            lowered_query = query.lower()
            lowered_raw = content.lower()

            self.__logger.debug('data - lowered_query: {0}'.format(lowered_query))
            self.__logger.debug('data - lowered_raw: {0}'.format(lowered_raw))

            if lowered_query in lowered_raw:
                count_entries += 1
                len_query = len(lowered_query)

                if skip_entries >= count_entries:
                    self.__logger.debug('data - item skipped}')
                    continue
                else:
                    self.__logger.debug('data - item added')

                index = lowered_raw.find(lowered_query, 0)

                extra = 70
                prefix = ''
                postfix = ''

                start = 0

                if index > extra:
                    self.__logger.debug('data - cutting text at the beginning')

                    prefix = '... '
                    start = index - extra

                if index + extra < len(content):
                    self.__logger.debug('data - cutting text at the end')

                    postfix = " ..."

                stop = start + (extra * 2) + len(query)

                self.__logger.debug('data - index: {0}'.format(index))
                self.__logger.debug('data - start: {0}'.format(start))
                self.__logger.debug('data - stop: {0}'.format(stop))

                # removing stuff until first blank
                for c in range(start, index):
                    if content[c:c + 1] == ' ':
                        self.__logger.debug('data - blank found: {0}'.format(c))
                        start = c
                        break

                # removing stuff until first blank, backwards
                for c in range(stop, index + len(query), -1):
                    if content[c:c + 1] == ' ':
                        self.__logger.debug('data - blank found: {0}'.format(c))
                        stop = c
                        break

                self.__logger.debug('data - spaced start: {0}'.format(start))
                self.__logger.debug('data - spaced stop: {0}'.format(stop))

                # vindevoy - 2020-05-06 - issue-187
                # Do not use replace on sample here because replace is case-sensitive
                sample = prefix + content[start:index] + '<b>' + content[index:index + len_query] + '</b>'
                sample += content[index + len_query:stop] + postfix

                self.__logger.debug('data - sample: {0}'.format(sample))

                occurrences = lowered_raw.count(lowered_query)
                self.__logger.debug('data - occurrences: {0}'.format(occurrences))

                if not cached_already:
                    meta['date'] = DateTimeSupport().rewrite_date(meta['date'])
                    # cached data has the correct format already

                entry = {
                    'item': item,
                    'meta': meta,
                    'occurrences': occurrences,
                    'sample': sample
                }

                data['found'].append(entry)

                if count_entries == (max_entries + skip_entries):
                    self.__logger.debug('data - enough posts')
                    break

        data['search'] = {'query': query}

        last_entry = count_entries

        data['pagination'] = {
            'current_page': page_index,
            'found_entries': count_entries - skip_entries,
            'max_entries': max_entries,
            'first_entry': first_entry,
            'last_entry': last_entry
        }

        return data

###
#
#   Version: 1.1.0
#   Date: 2020-05-01
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Rewrite date format
#       - Uses data cacher
#
#   Version: 1.0.0
#   Date: 2020-04-26
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Searching on posts
#       - Searching on pages
#
###
