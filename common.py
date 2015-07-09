__author__ = 'Francesco Infante'


class Configuration(object):
    def __init__(self, **rules):
        self.rules = rules


class Call(object):
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs


class Path(object):
    def __init__(self, path):
        self.path = path
