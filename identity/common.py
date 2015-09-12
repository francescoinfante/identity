__author__ = 'Francesco Infante'

import ujson

from dpath import util


class Configuration(dict):
    def __init__(self, *args, **kwargs):
        super(Configuration, self).__init__(*args, **kwargs)


class Path(str):
    def __init__(self, *args, **kwargs):
        super(Path, self).__init__(*args, **kwargs)


def extract_from_tuple(data, path):
    """
    Args:
        data (tuple): tuple of records
        path (Path): attribute to extract

    Returns:
        tuple: one attribute for record

    Example:
        data: ({'a':2, 'b':3}, {'a':1, 'b':2})
        path: 'a'
        returns: (2, 1)
    """
    result = []

    for x in data:
        try:
            result.append(util.get(x, path))
        except:
            result.append(None)

    return tuple(result)


class JSONSource(object):
    """
    Read from a file where each line is a document represented as a JSON object.

    Args:
        filename (str)
    """

    def __init__(self, filename):
        self.file = open(filename)

    def next(self):
        return ujson.loads(self.file.next())

    def __iter__(self):
        return self
