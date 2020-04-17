###
#
#   Full history: see below
#
#   Version: 1.0.0
#   Date: 2020-04-15
#   Author: Yves Vindevogel (vindevoy)
#
###

import cherrypy
import logging
import logging.config
import os
import yaml

from common.options import Options

# https://stackoverflow.com/questions/41879512/cherrypy-is-not-respecting-desired-logging-format


class LoggingLoader:
    # No need to log anything, the loader is not yet loaded so you don't have a logger

    @staticmethod
    def configure():
        cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)

        # DO NOT USE Content() here, it's not ready
        settings_file = os.path.join(Options().data_dir, 'logging', 'settings.yml')
        file = open(settings_file, 'r')
        settings_yaml = yaml.load(file.read(), Loader=yaml.SafeLoader)

        logging.config.dictConfig(settings_yaml)

        Options().default_logging_level = settings_yaml['loggers']['']['level']
