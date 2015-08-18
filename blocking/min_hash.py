__author__ = 'Francesco Infante'

import random
import string
import hashlib
from itertools import combinations

import dpath.util

from api import Blocking


class HashFamily(object):
    def __init__(self, size):
        self._salt = [''.join(random.choice(string.ascii_uppercase) for _ in range(5)) for _ in range(size)]

    def __getitem__(self, k):
        if k >= len(self._salt):
            raise IndexError()
        return lambda x: hashlib.sha1(str(x) + self._salt[k]).hexdigest()[-8:].zfill(8)

    @staticmethod
    def max_value():
        return 'ffffffff'


class MinHash(Blocking):
    """
    Algorithm based on Broder et al. (1998); Rajaraman et al. (2012).

    Args:
        source (list(dict)): list of records
        attribute (Path): attribute (a set) used to compute the sketch
        bands (int): number of bands for LSH
        rows (int): number of rows for LSH
    """

    def __init__(self, source, attribute, bands, rows):
        hash_family = HashFamily(bands * rows)
        sketches = []
        buckets = {}

        for e in source:
            s = dpath.util.get(e, attribute)

            sketch = []

            for hash_function in hash_family:
                current_min = HashFamily.max_value()
                for y in s:
                    current_min = min(current_min, hash_function(y))
                sketch.append(str(current_min))

            sketches.append((e, sketch))

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

        self._buckets = buckets.itervalues()

    def next(self):
        return self._buckets.next()
