###
#
#   Full history: see below
#
#   Version: 1.0.0
#   Date: 2020-05-08
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Mapping of URLs to physical files
#
###

import logging

from common.options import Options
from common.content import Content
from common.singleton import Singleton


class Mapping(metaclass=Singleton):
    __base_dir = 'mapping'
    __logger = None

    incoming = None
    outgoing = None

    def __init__(self):
        self.__logger = logging.getLogger('MODEL.MAPPING')
        self.__logger.setLevel(Options().default_logging_level)

        self.__data()

    def __data(self):
        content = Content().load_data_settings_yaml(self.__base_dir)
        self.__logger.debug('__data - content: {0}'.format(content))

        incoming = {}
        outgoing = {}

        for mapping in content['content']:
            self.__logger.debug('__data - mapping: {0}'.format(mapping))

            target = mapping['target']
            source = mapping['source']

            if target[0:1] != '/':
                target = '/{0}'.format(target)

            if source[0:1] != '/':
                source = '/{0}'.format(source)

            self.__logger.debug('__data - target: {0}'.format(target))
            self.__logger.debug('__data - source: {0}'.format(source))

            incoming[target] = source
            self.__logger.info('mapping incoming URL \'{0}\' to source \'{1}\''.format(target, source))

            outgoing[source] = target
            self.__logger.info('mapping outgoing source \'{0}\' to URL \'{1}\''.format(source, target))

        self.incoming = incoming
        self.outgoing = outgoing
