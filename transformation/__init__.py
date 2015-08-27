__author__ = 'Francesco Infante'

from multiprocessing import Pool, cpu_count
from itertools import izip, repeat

from dpath import util

from common import Configuration, Apply, Path


def _transform(args):
    data = args[0]
    config = args[1]

    result = config
    if isinstance(config, Configuration):
        result = {k: _transform((data, v)) for k, v in config.iteritems()}
    elif isinstance(config, Apply):
        args = [_transform((data, v)) for v in config.args]
        kwargs = {k: _transform((data, v)) for k, v in config.kwargs.iteritems()}
        result = config.function(*args, **kwargs)
    elif isinstance(config, Path):
        try:
            result = util.get(data, config)
        except:
            result = None

    return result


class DataTransformation(object):
    """
    Args:
        source ([dict]): list of records
        config (Configuration): configuration to apply to each record
    """

    def __init__(self, source, config, processes=cpu_count()):
        self.pool = Pool(processes)
        self.results = self.pool.imap(_transform, izip(source, repeat(config)))

    def next(self):
        return self.results.next()

    def __del__(self):
        self.pool.close()


if __name__ == "__main__":
    pass
