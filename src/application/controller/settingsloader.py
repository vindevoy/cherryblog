###
#
#   Full history: see below
#
#   Version: 1.2.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Split between the properties needed by the engine and needed by the application
#
###

import os

from common.content import Content
from common.options import Options
from common.singleton import Singleton


class SettingsLoader(metaclass=Singleton):
    __environment = None

    def __init__(self, environment):
        self.__environment = environment

    def parse(self):
        # data_dir and environment are set before the SettingsLoader is called
        # and are read in application.py where the command line is parsed
        environment_dir = os.path.join(Options().data_dir, 'environment')

        # read the yaml file
        settings_yaml = Content().load_yaml(environment_dir, '{0}.yml'.format(self.__environment))

        # set the settings needed elsewhere in the code
        self.__option_settings(settings_yaml)

        # return the settings really needed in a format for CherryPy
        # they will be used when starting the engine in application.py
        return self.__engine_settings(settings_yaml)

    @staticmethod
    def __engine_settings(settings_yaml):
        global_settings = {
            'server.socket_host': settings_yaml['server']['socket_host'],
            'server.socket_port': settings_yaml['server']['socket_port'],
            'server.thread_pool': settings_yaml['server']['thread_pool'],
            'engine.autoreload.on': settings_yaml['engine']['autoreload'],
        }

        settings = {
            'global': global_settings
        }

        for staticdir in settings_yaml['tools']['staticdirs']:
            url = staticdir['url']
            absolute = staticdir['absolute']
            path = staticdir['path']

            if not absolute:
                path = os.path.join(os.getcwd(), path)

            settings[url] = {'tools.staticdir.on': True,
                             'tools.staticdir.dir': path}

        settings['/favicon.ico'] = {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(Options().data_dir, 'images', 'favicon.ico')
        }

        return settings

    @staticmethod
    def __option_settings(settings_yaml):
        if settings_yaml['directories']['theme']['absolute']:
            Options().theme_dir = settings_yaml['directories']['theme']['path']
        else:
            Options().theme_dir = os.path.join(os.getcwd(), settings_yaml['directories']['theme']['path'])

        if settings_yaml['directories']['log']['absolute']:
            Options().log_dir = settings_yaml['directories']['log']['path']
        else:
            Options().log_dir = os.path.join(os.getcwd(), settings_yaml['directories']['log']['path'])

        if settings_yaml['directories']['run']['absolute']:
            Options().run_dir = settings_yaml['directories']['run']['path']
        else:
            Options().run_dir = os.path.join(os.getcwd(), settings_yaml['directories']['run']['path'])

        Options().meta_content_separator = settings_yaml['content']['meta_content_separator']

        Options().daemon = settings_yaml['engine']['daemon']

        Options().privileges = settings_yaml['user']['privileges']
        Options().uid = settings_yaml['user']['uid']
        Options().gid = settings_yaml['user']['gid']

###
#
#   Version: 1.1.0
#   Date: 2020-04-09
#   Author: Yves Vindevogel (vindevoy)
#
#   Fixes:
#       - Used os.path.join in parse. It has a slash in it and formats.
#       - Dynamic paths to themes and data
#
#   Version: 1.0.1
#   Date: 2020-04-08
#   Author: Yves Vindevogel (vindevoy)
#
#   Fixes:
#       - Used os.path.join in parse. It has a slash in it and formats.
#
#   Version: 1.0.0
#   Date: 2020-04-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Original code
#
###
