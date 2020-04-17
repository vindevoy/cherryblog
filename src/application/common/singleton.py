###
#
#   Version: 1.0.0
#   Date: 2020-04-07
#   Author: Yves Vindevogel (vindevoy)
#
#   Purpose: create a singleton class that can be re-used as metaclass by others to make them singletons
#   https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python (method 3)
#
###


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
