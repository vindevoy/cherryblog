###
#
#   Full history: see below
#
#   Version: 1.1.0
#   Date: 2020-04-13
#   Author: Yves Vindevogel (vindevoy)
#
#   Features:
#       - Extra properties for
#           - Daemon
#           - Extra directories
#           - privileges (starting as root, lower to other user and group)
#
###

from singleton import Singleton


class OptionsLoader(metaclass=Singleton):
    # Will be used for loading the correct file
    environment = ''

    # Directories set through the command line
    data_dir = ''

    # Directories set from the settings file (environment.yml)
    theme_dir = ''
    log_dir = ''
    run_dir = ''

    # Properties set from the settings file (environment.yml)
    daemon = False

    # User privileges can be used to start as root and run on port 80 (privileged port)
    # and then run with a user with less rights
    privileges = False
    uid = 0
    gid = 0

###
#
#   Version: 1.0.0
#   Date: 2020-04-09
#   Author: Yves Vindevogel (vindevoy)
#
#   Original code
###

