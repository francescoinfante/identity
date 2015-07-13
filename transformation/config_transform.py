__author__ = 'Francesco Infante'

import multiprocessing
from multiprocessing import Pool
from itertools import izip, repeat

import dpath.util

from api import Transformation
from common import Configuration, Apply, Path


def _transform(args):
    data = args[0]
    config = args[1]

    result = config
    if isinstance(config, Configuration):
        result = {k: _transform((data, v)) for k, v in config.rules.iteritems()}
    elif isinstance(config, Apply):
        args = [_transform((data, v)) for v in config.args]
        kwargs = {k: _transform((data, v)) for k, v in config.kwargs.iteritems()}
        result = config.function(*args, **kwargs)
    elif isinstance(config, Path):
        try:
            result = dpath.util.get(data, config.path)
        except KeyError:
            result = None

    return result


class ConfigTransform(Transformation):
    """
    Apply the configuration to each entry of the source
    """

    def __init__(self, source, config, processes=multiprocessing.cpu_count()):
        self.pool = Pool(processes)
        self.results = self.pool.imap(_transform, izip(source, repeat(config)))

    def next(self):
        return self.results.next()

    def __del__(self):
        self.pool.close()
