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

    def __init__(self, source, attributes, no_none=False, debug=False, filter_size=0, string_as_list=False):
        buckets = {}
        blocking_keys = {}

        count = 0

        for e in source:

            count += 1

            if debug and count % 1000 == 0:
                logger.info('tick ' + str(count))

            keys = [[]]
            for a in attributes:
                v = None
                try:
                    v = util.get(e, a)
                except:
                    pass
                if string_as_list and isinstance(v, basestring):
                    v = v.split(' ')
                if isinstance(v, list):
                    new_keys = []
                    for x in keys:
                        for y in v:
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
                if len(buckets[k]) == 1:
                    break
                logger.info(str(blocking_keys[k]) + ' appears ' + str(len(buckets[k])) + ' times')

        count = 0

        new_buckets = {}

        for k, v in buckets.iteritems():
            size = (len(v) * (len(v) - 1)) / 2
            if filter_size == 0 or size <= filter_size:
                count += size
                new_buckets[k] = combinations(v, 2)

        if debug:
            logger.info("# candidate pairs: " + str(count))

        self._buckets = new_buckets.itervalues()

    def next(self):
        return self._buckets.next()
