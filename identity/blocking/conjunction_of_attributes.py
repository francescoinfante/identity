__author__ = 'Francesco Infante'

from itertools import combinations
import logging

from dpath import util

logger = logging.getLogger(__name__)
from api import Blocking


class ConjunctionOfAttributes(Blocking):
    """
    Args:
        source ([dict]): list of records
        attributes (list(Path)): list of attributes to use as blocking key
    """

    def __init__(self, source, attributes, no_none=False, debug=False):
        buckets = {}
        blocking_keys = {}
        for e in source:
            tmp = []
            for a in attributes:
                try:
                    tmp.append(util.get(e, a))
                except:
                    tmp.append(None)
            if no_none and None in tmp:
                continue
            h = hash(tuple(tmp))
            if h not in blocking_keys:
                blocking_keys[h] = tmp
            if h in buckets:
                buckets[h].append(e)
            else:
                buckets[h] = [e]

        if debug:
            for k, v in buckets.iteritems():
                logger.info(blocking_keys[k] + ' appears ' + str(len(v)) + ' times')

        print len(buckets)

        for k, v in buckets.iteritems():
            buckets[k] = combinations(v, 2)

        self._buckets = buckets.itervalues()

    def next(self):
        return self._buckets.next()
