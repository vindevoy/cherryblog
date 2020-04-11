###
#
#   Full history: see below
#
#   Version: 1.1.0
#   Date: 2020-04-09
#   Author: Yves Vindevogel (vindevoy)
#
#   Fixes:
#       - Used os.path.join in parse. It has a slash in it and formats.
#       - Dynamic paths to themes and data
#
###

import os
import yaml

from optionsloader import OptionsLoader
from singleton import Singleton


class SettingsLoader(metaclass=Singleton):
    __environment = None

    def __init__(self, environment):
        self.__environment = environment

    def parse(self):
        environment_dir = os.path.join(OptionsLoader().data_dir, 'environment')
        environment_file = os.path.join(environment_dir, '{0}.yml'.format(self.__environment))

        file = open(environment_file, 'r')
        settings_yaml = yaml.load(file.read(), Loader=yaml.SafeLoader)

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
            'tools.staticfile.filename': os.path.join(OptionsLoader().data_dir, 'images', 'favicon.ico')
        }

        return settings

###
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
