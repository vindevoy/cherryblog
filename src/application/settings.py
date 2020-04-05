###
#
#   Version: 1.0.0
#   Date: 2020-03-29
#   Author: Yves Vindevogel (vindevoy)
#
###

import os
import socket

from singleton import Singleton


class Settings(metaclass=Singleton):
    __config = {}

    def __init__(self):
        self.__config = {
            'global': {
                'server.socket_host': '127.0.0.1',
                'server.socket_port': 8080,
                'server.thread_pool': 8,

                'engine.autoreload.on': True,
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(self.root_dir, 'src', 'theme', 'default', 'static')
            },
            '/images': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(self.root_dir, 'src', 'data', 'images')
            }
        }

    @property
    def server_config(self):
        return self.__config

    @property
    def root_dir(self):
        return os.getcwd()

    @property
    def index_max_posts(self):
        return 4

    @property
    def index_spotlight_posts(self):
        return 1

    @property
    def index_highlight_posts(self):
        return 2
