__author__ = 'Francesco Infante'

from dpath import util


class Configuration(dict):
    def __init__(self, *arg, **kw):
        super(Configuration, self).__init__(*arg, **kw)


class Path(str):
    def __init__(self, *arg, **kw):
        super(Path, self).__init__(*arg, **kw)


class Apply(object):
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs


def extract_from_tuple(data, path):
    """
    Args:
        data (tuple): tuple of records (dicts)
        path (Path): path of the attributes to extract

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
