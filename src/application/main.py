###
#
#   Full history: see below
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

import cherrypy
import getopt
import logging
import os
import sys

from cherrypy.process.plugins import Daemonizer, PIDFile, DropPrivileges

from controller.application import Application
from common.logging_loader import LoggingLoader
from common.options import Options
from controller.settingsloader import SettingsLoader


if __name__ == '__main__':
    LoggingLoader().configure()

    logger = logging.getLogger('MAIN')

    environment = 'localhost'
    data_dir = ""

    opts, args = getopt.getopt(sys.argv[1:], 'd:e:', ['env=', 'data='])
    logger.debug('opts: {0}'.format(opts))
    logger.debug('args: {0}'.format(args))

    for opt, arg in opts:
        if opt in ['-d', '--data']:
            logger.debug('Overriding data_dir to {0}.'.format(arg))
            data_dir = arg
        if opt in ['-e', '--env']:
            logger.debug('Overriding environment to {0}.'.format(arg))
            environment = arg

    if data_dir == '':
        data_dir = os.path.join(os.getcwd(), 'src', 'data')

    logger.info('Environment set to {0}.'.format(environment))
    logger.info('Data directory set to {0}.'.format(data_dir))

    Options().environment = environment
    Options().data_dir = data_dir

    settings = SettingsLoader(environment).parse()

    if Options().daemon:
        daemon = Daemonizer(cherrypy.engine)
        daemon.subscribe()
    else:
        logger.info('Not running as daemon.')

    pid = PIDFile(cherrypy.engine, os.path.join(Options().run_dir, 'cherryblog.pid'))
    pid.subscribe()

    if Options().privileges:
        privileges = DropPrivileges(cherrypy.engine, uid=Options().uid, gid=Options().gid)
        privileges.subscribe()
    else:
        logger.info('No user privileges specified.')

    cherrypy.quickstart(Application(), config=settings)
