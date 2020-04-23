###
#
#   Full history: see below
#
#   Version: 1.3.0
#   Date: 2020-04-23
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       SSL
#
###

import os
import yaml

# NEVER IMPORT Content from common.content => you need settings from this class here

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
        # DO NOT USE the Content() class here, it needs the settings itself to set the logging level
        settings_file = os.path.join(environment_dir, '{0}.yml'.format(self.__environment))
        file = open(settings_file, 'r')
        settings_yaml = yaml.load(file.read(), Loader=yaml.SafeLoader)

        # set the settings needed elsewhere in the code
        self.__option_settings(settings_yaml)

        # Return the settings really needed in a format for CherryPy
        # They will be used when starting the engine in application.py
        # They are logged in main.py
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

        try:
            for staticdir in settings_yaml['tools']['staticdirs']:
                url = staticdir['url']
                absolute = staticdir['absolute']
                path = staticdir['path']

                if not absolute:
                    path = os.path.abspath(os.path.join(os.getcwd(), path))

                settings[url] = {'tools.staticdir.on': True,
                                 'tools.staticdir.dir': path}
        except KeyError:
            pass

        try:
            for staticfile in settings_yaml['tools']['staticfiles']:
                url = staticfile['url']
                absolute = staticfile['absolute']
                path = staticfile['path']

                if not absolute:
                    path = os.path.abspath(os.path.join(os.getcwd(), path))

                settings[url] = {'tools.staticfile.on': True,
                                 'tools.staticfile.filename': path}
        except KeyError:
            pass

        settings['/favicon.ico'] = {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.abspath(os.path.join(Options().data_dir, 'images', 'favicon.ico'))
        }

        return settings

    @staticmethod
    def __option_settings(settings_yaml):
        # The individual properties are logged in main
        # No need to log them here
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

        Options().ssl_certificate = settings_yaml['ssl']['ssl_certificate']
        Options().ssl_private_key = settings_yaml['ssl']['ssl_private_key']
        Options().ssl_certificate_chain = settings_yaml['ssl']['ssl_certificate_chain']

        use_ssl = False

        if Options().ssl_certificate != '':
            use_ssl = True

        if Options().ssl_private_key != '':
            use_ssl = True

        if Options().ssl_certificate_chain != '':
            use_ssl = True

        Options().use_ssl = use_ssl

###
#
#   Version: 1.2.1
#   Date: 2020-04-15
#   Author: Yves Vindevogel (vindevoy)
#
#   Changes:
#       Because of logging, the Content() class cannot be used
#
#   Version: 1.2.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Split between the properties needed by the engine and needed by the application
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
