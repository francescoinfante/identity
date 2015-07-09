__author__ = 'Francesco Infante'

import dpath.util

from api import Transformation


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


class ConfigTransform(Transformation):
    """
    Apply the configuration to each entry of the source
    """

    def __init__(self, source, config):
        self.source = source
        self.config = config

    def _transform(self, data, config=None):
        if config is None:
            config = self.config

        if isinstance(config, Configuration):
            return {k: self._transform(data, v) for k, v in config.rules.iteritems()}
        elif isinstance(config, Call):
            args = [self._transform(data, v) for v in config.args]
            kwargs = {k: self._transform(data, v) for k, v in config.kwargs.iteritems()}
            return config.function(*args, **kwargs)
        elif isinstance(config, Path):
            return dpath.util.get(data, config.path)

        return config

    def next(self):
        return self._transform(self.source.next())
