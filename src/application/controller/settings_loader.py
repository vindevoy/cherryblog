###
#
#   Full history: see below
#
#   Version: 1.5.0
#   Date: 2020-04-28
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       Handling missing keys and using defaults
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
        # defaults
        try:
            socket_host = settings_yaml['server']['socket_host']
        except KeyError:
            socket_host = '127.0.0.1'

        try:
            socket_port = settings_yaml['server']['socket_port']
        except KeyError:
            socket_port = 8080

        try:
            thread_pool = settings_yaml['server']['thread_pool']
        except KeyError:
            thread_pool = 8

        try:
            autoreload = settings_yaml['engine']['autoreload']
        except KeyError:
            autoreload = True

        global_settings = {
            'server.socket_host': socket_host,
            'server.socket_port': socket_port,
            'server.thread_pool': thread_pool,
            'engine.autoreload.on': autoreload,
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

        try:
            settings['/favicon.ico'] = {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': os.path.abspath(os.path.join(Options().data_dir, 'images', 'favicon.ico'))
            }
        except FileNotFoundError:
            pass

        return settings

    @staticmethod
    def __option_settings(settings_yaml):
        # The individual properties are logged in main
        # No need to log them here

        try:
            Options().theme_dir = settings_yaml['directories']['theme']['path']
        except KeyError:
            Options().theme_dir = os.path.join(os.getcwd(), settings_yaml['directories']['theme']['path'])

        try:
            Options().log_dir = settings_yaml['directories']['log']['path']
        except KeyError:
            Options().log_dir = os.path.join(os.getcwd(), settings_yaml['directories']['log']['path'])

        try:
            Options().run_dir = settings_yaml['directories']['run']['path']
        except KeyError:
            Options().run_dir = os.path.join(os.getcwd(), settings_yaml['directories']['run']['path'])

        try:
            Options().meta_content_separator = settings_yaml['content']['meta_content_separator']
        except KeyError:
            Options().meta_content_separator = '__________'

        try:
            Options().daemon = settings_yaml['engine']['daemon']
        except KeyError:
            Options().daemon = False

        try:
            Options().privileges = settings_yaml['user']['privileges']
        except KeyError:
            Options().privileges = False

        try:
            Options().uid = settings_yaml['user']['uid']
        except KeyError:
            Options().uid = 0

        try:
            Options().gid = settings_yaml['user']['gid']
        except KeyError:
            Options().gid = 0

        try:
            use_ssl = False

            Options().ssl_certificate = settings_yaml['ssl']['ssl_certificate']
            Options().ssl_private_key = settings_yaml['ssl']['ssl_private_key']
            Options().ssl_certificate_chain = settings_yaml['ssl']['ssl_certificate_chain']

            if Options().ssl_certificate != '':
                use_ssl = True

            if Options().ssl_private_key != '':
                use_ssl = True

            if Options().ssl_certificate_chain != '':
                use_ssl = True

        except KeyError:
            use_ssl = False

        Options().use_ssl = use_ssl

        try:
            Options().caching = settings_yaml['caching']['use']
        except KeyError:
            Options().caching = False

###
#
#   Version: 1.4.0
#   Date: 2020-04-23
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       Caching enabled or not
#
#   Version: 1.3.0
#   Date: 2020-04-23
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       SSL
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
