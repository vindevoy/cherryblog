import logging.config
import cherrypy

from common.content import Content

# https://stackoverflow.com/questions/41879512/cherrypy-is-not-respecting-desired-logging-format


class LoggingLoader:
    @staticmethod
    def configure():
        cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)

        logging_settings = Content().load_yaml('./src/data/logging', 'settings.yml')
        logging.config.dictConfig(logging_settings)
