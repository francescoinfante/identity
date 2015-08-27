__author__ = 'Francesco Infante'

from itertools import combinations

from dpath import util

from api import Blocking


class SortedNeighborhood(Blocking):
    """
    Algorithm based on Hernandez and Stolfo (1995).

    Args:
        source ([dict]): list of records
        key (Path): attribute to use as key
        window_size (int)
    """

    def __init__(self, source, key, window_size):
        l = []
        for e in source:
            key_value = util.get(e, key)
            l.append((key_value, e))
        ordered_list = sorted(l)
        buckets = {}

        for i in range(0, len(ordered_list) - 1):
            buckets[i] = []
            for j in range(0, window_size):
                if len(ordered_list) > i + j:
                    buckets[i].append(ordered_list[i + j][1])

        for k, v in buckets.iteritems():
            buckets[k] = combinations(v, 2)

        self._buckets = buckets.itervalues()

    def next(self):
        return self._buckets.next()
