__author__ = 'Francesco Infante'

from itertools import combinations

from dpath import util

from api import Blocking


class ConjunctionOfAttributes(Blocking):
    """
    Args:
        source ([dict]): list of records
        attributes (list(Path)): list of attributes to use as blocking key
    """

    def __init__(self, source, attributes, no_none=False):
        buckets = {}
        for e in source:
            tmp = []
            for a in attributes:
                try:
                    tmp.append(util.get(e, a))
                except:
                    tmp.append(None)
            h = hash(tuple(tmp))
            if h in buckets:
                buckets[h].append(e)
            else:
                buckets[h] = [e]

        if no_none and None in buckets:
            del buckets[None]

        for k, v in buckets.iteritems():
            buckets[k] = combinations(v, 2)

        self._buckets = buckets.itervalues()

    def next(self):
        return self._buckets.next()
