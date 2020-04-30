###
#
#   Full history: see below
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

import logging

from pathlib import Path

from common.content import Content
from common.options import Options
from common.singleton import Singleton


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

            meta, raw, html = Content().read_content(directory, file)

            lowered_query = query.lower()
            lowered_raw = raw.lower()

            self.__logger.debug('data - lowered_query: {0}'.format(lowered_query))
            self.__logger.debug('data - lowered_raw: {0}'.format(lowered_raw))

            if lowered_query in lowered_raw:
                count_entries += 1

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

                if index + extra < len(raw):
                    self.__logger.debug('data - cutting text at the end')

                    postfix = " ..."

                stop = start + (extra * 2) + len(query)

                self.__logger.debug('data - index: {0}'.format(index))
                self.__logger.debug('data - start: {0}'.format(start))
                self.__logger.debug('data - stop: {0}'.format(stop))

                # removing stuff until first blank
                for c in range(start, index):
                    if raw[c:c+1] == ' ':
                        self.__logger.debug('data - blank found: {0}'.format(c))
                        start = c
                        break

                # removing stuff until first blank, backwards
                for c in range(stop, index + len(query), -1):
                    if raw[c:c+1] == ' ':
                        self.__logger.debug('data - blank found: {0}'.format(c))
                        stop = c
                        break

                self.__logger.debug('data - spaced start: {0}'.format(start))
                self.__logger.debug('data - spaced stop: {0}'.format(stop))

                sample = prefix + raw[start:stop] + postfix
                self.__logger.debug('data - sample: {0}'.format(sample))

                sample = sample.replace(query, '<b>{0}</b>'.format(query))
                self.__logger.debug('data - bold sample: {0}'.format(sample))

                occurrences = lowered_raw.count(lowered_query)
                self.__logger.debug('data - occurrences: {0}'.format(occurrences))

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
