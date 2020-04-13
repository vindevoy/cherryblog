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
import os
import sys

from cherrypy.process.plugins import Daemonizer, PIDFile, DropPrivileges

from controller.application import Application
from controller.options import Options
from controller.settingsloader import SettingsLoader


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

    Options().environment = environment
    Options().data_dir = data_dir

    settings = SettingsLoader(environment).parse()

    if Options().daemon:
        daemon = Daemonizer(cherrypy.engine)
        daemon.subscribe()

    pid = PIDFile(cherrypy.engine, os.path.join(Options().run_dir, 'cherryblog.pid'))
    pid.subscribe()

    if Options().privileges:
        privileges = DropPrivileges(cherrypy.engine, uid=Options().uid, gid=Options().gid)
        privileges.subscribe()

    cherrypy.quickstart(Application(), config=settings)
