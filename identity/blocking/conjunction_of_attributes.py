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
            keys = [[]]
            for a in attributes:
                v = None
                try:
                    v = util.get(e, a)
                except:
                    pass
                if isinstance(v, list):
                    new_keys = []
                    for x in keys:
                        for y in v:
                            if isinstance(y, list):
                                y = str(y)
                            new_keys.append(x + [y])
                    keys = new_keys
                else:
                    for x in keys:
                        x.append(v)
            for tmp in keys:
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
            for k in sorted(buckets, key=lambda k: len(buckets[k]), reverse=True):
                logger.info(str(blocking_keys[k]) + ' appears ' + str(len(buckets[k])) + ' times')

        count = 0

        for k, v in buckets.iteritems():
            buckets[k] = combinations(v, 2)
            count += (len(v) * (len(v) - 1)) / 2

        if debug:
            logger.info("# candidate pairs: " + str(count))

        self._buckets = buckets.itervalues()

    def next(self):
        return self._buckets.next()
