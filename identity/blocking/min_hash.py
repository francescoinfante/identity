__author__ = 'Francesco Infante'

from random import choice
from string import ascii_uppercase
from hashlib import sha1
from itertools import combinations
import logging

from dpath import util

from api import Blocking

logger = logging.getLogger(__name__)


class HashFamily(object):
    def __init__(self, size):
        self._salt = [(''.join(choice(ascii_uppercase) for _ in range(5))) for _ in range(size)]

    def __getitem__(self, k):
        if k >= len(self._salt):
            raise IndexError()
        return lambda x: sha1(str(x) + self._salt[k]).hexdigest()[-8:].zfill(8)

    @staticmethod
    def max_value():
        return 'ffffffff'


class MinHash(Blocking):
    """
    Algorithm based on Broder et al. (1998); Rajaraman et al. (2012).

    Args:
        source ([dict]): list of records
        attribute (Path): attribute on which to compute the sketch
        bands (int)
        rows (int)
    """

    def __init__(self, source, attribute, bands, rows, debug=False):
        hash_family = HashFamily(bands * rows)
        sketches = []
        buckets = {}

        count = 0

        if debug:
            logger.info('computing sketches')

        for e in source:

            count += 1

            if debug and count % 1000 == 0:
                logger.info('tick ' + count)

            try:
                s = util.get(e, attribute)
            except:
                continue

            sketch = []

            for hash_function in hash_family:
                current_min = HashFamily.max_value()
                for y in s:
                    current_min = min(current_min, hash_function(y))
                sketch.append(str(current_min))

            sketches.append((e, sketch))

        if debug:
            logger.info('all sketches done')

        for b in range(0, bands):
            tmp_buckets = {}
            for e, sketch in sketches:
                s = ""
                for x in range(0, rows):
                    s += sketch[b * rows + x]
                if s in tmp_buckets:
                    tmp_buckets[s].append(e)
                else:
                    tmp_buckets[s] = [e]
            for k, v in tmp_buckets.iteritems():
                buckets[str(b) + k] = v

        for k, v in buckets.iteritems():
            buckets[k] = combinations(v, 2)

        if debug:
            logger.info('minhash done')

        self._buckets = buckets.itervalues()

    def next(self):
        return self._buckets.next()
