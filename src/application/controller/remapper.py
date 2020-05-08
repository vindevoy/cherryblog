###
#
#   Version: 1.0.0
#   Date: 2020-05-08
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       Remapping of incoming requests to content documents
#       Remapping of content to outgoing URLs
#
###

import logging

from common.options import Options
from common.singleton import Singleton


class Remapper(metaclass=Singleton):
    outgoing_content = None
    incoming_content = None

    __logger = None

    def __init__(self):
        self.__logger = logging.getLogger('REMAPPER')
        self.__logger.setLevel(Options().default_logging_level)

    def remap_document(self, doc):
        self.__logger.debug('remap_document - doc: {0}'.format(doc))

        return self.__remap(doc, self.outgoing_content, 'OUT')

    def remap_url(self, url):
        self.__logger.debug('remap_url - url: {0}'.format(url))

        return self.__remap(url, self.incoming_content, 'IN')

    def __remap(self, mapping, mappings, way):
        self.__logger.debug('__remap - mapping: {0}'.format(mapping))
        self.__logger.debug('__remap - mappings: {0}'.format(mappings))

        if mapping in mappings:
            mapped = mappings[mapping]
            self.__logger.debug('__remap - mapped: {0}'.format(mapped))

            self.__logger.info('{0}: {1} -> {2}'.format(way, mapping, mapped))
            return mapped
        else:
            return mapping
