###
#
#   Full history: see below
#
#   Version: 2.2.0
#   Date: 2020-04-23
#   Author: Yves Vindevogel (vindevoy)
#
#   Added SSL
#
###

import cherrypy
import getopt
import logging
import os
import sys

from cherrypy.process.plugins import Daemonizer, PIDFile, DropPrivileges

from controller.application import Application
from controller.logging_loader import LoggingLoader
from common.options import Options
from controller.settings_loader import SettingsLoader

__application = 'CherryBlog'
__version = '1.2.0'

if __name__ == '__main__':
    environment = 'localhost'
    data_dir = ""

    opts, args = getopt.getopt(sys.argv[1:], 'd:e:', ['env=', 'data='])

    for opt, arg in opts:
        if opt in ['-d', '--data']:
            data_dir = arg
        if opt in ['-e', '--env']:
            environment = arg

    if data_dir == '':
        data_dir = os.path.join(os.getcwd(), 'src', 'data')

    # Options is a singleton and can be loaded with what we know already
    Options().environment = environment
    Options().data_dir = data_dir

    # Load the settings from the environment.yml file to fill out the rest of the settings
    # This also sets most of the unknown properties in Options()
    settings = SettingsLoader(environment).parse()

    # Do not load the logging before you have the data_dir
    # This will fill out the logging level in the Options()
    LoggingLoader().configure()

    logger = logging.getLogger('MAIN')

    logger.info('{0} v.{1}'.format(__application, __version))
    logger.info('Environment set to {0}.'.format(environment))
    logger.info('Data directory set to {0}.'.format(data_dir))
    logger.info('Theme directory set to {0}.'.format(Options().theme_dir))
    logger.info('Log directory set to {0}.'.format(Options().log_dir))
    logger.info('Run directory set to {0}.'.format(Options().run_dir))
    logger.info('Meta-content separator set to {0}.'.format(Options().meta_content_separator))
    logger.info('Default logging level set to {0}.'.format(Options().default_logging_level))

    logger.debug('main - CherryPy settings:\n{0}\n'.format(settings))

    if Options().use_ssl:
        cherrypy.server.ssl_module = 'pyOpenSSL'

        if Options().ssl_certificate != '':
            cherrypy.server.ssl_certificate = Options().ssl_certificate

        if Options().ssl_private_key != '':
            cherrypy.server.ssl_private_key = Options().ssl_private_key

        if Options().ssl_certificate_chain != '':
            cherrypy.server.ssl_certificate_chain = Options().ssl_certificate_chain

    if Options().daemon:
        # Daemon info is logged by CherryPy
        daemon = Daemonizer(cherrypy.engine)
        daemon.subscribe()
    else:
        logger.info('Not running as daemon.')

    # PID is logged by CherryPy
    pid = PIDFile(cherrypy.engine, os.path.join(Options().run_dir, 'cherryblog.pid'))
    pid.subscribe()

    if Options().privileges:
        # Privileges are logged by CherryPy
        privileges = DropPrivileges(cherrypy.engine, uid=Options().uid, gid=Options().gid)
        privileges.subscribe()
    else:
        logger.info('No user privileges specified.')

    cherrypy.quickstart(Application(), config=settings)

###
#
#   Version: 2.1.0
#   Date: 2020-04-15
#   Author: Yves Vindevogel (vindevoy)
#
#   Added logging
#
#   Version: 2.0.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   main.py is the entry point of the application and is derived from the original application.py file
#   It has been split into main.py containing only the main() function
#   and application.py in controller that maps the URLs
#   History of the file is kept in application.py
#
###