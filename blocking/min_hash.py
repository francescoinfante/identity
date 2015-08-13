__author__ = 'Francesco Infante'

import random
import sys
import itertools

import dpath.util

from api import Blocking

_memo_mask = {}


def hash_family(n):
    mask = _memo_mask.get(n)
    if mask is None:
        random.seed(n)
        mask = _memo_mask[n] = random.getrandbits(64)

    def hash_function(x):
        return hash(x) ^ mask

    return hash_function


class MinHash(Blocking):
    """
    Algorithm based on Broder et al. (1998); Rajaraman et al. (2012).

    It takes as arguments the documents, the attribute (instance of Path) on which to compute the sketch,
    the number of bands and the number of rows.

    The attribute must be a set.

    It returns all the pairs that match on at least one band (Non-disjoint blocking).
    """

    def __init__(self, source, attribute, bands, rows):
        n = bands * rows
        pairs = set()
        sketches = []

        for e in source:
            s = dpath.util.get(e, attribute.path)

            sketch = []

            for x in range(0, n):
                hash_function = hash_family(x)
                current_min = sys.maxint
                for y in s:
                    current_min = min(current_min, hash_function(y))
                sketch.append(str(current_min))

            sketches.append((e, sketch))

        for b in range(0, bands):
            buckets = {}
            for e, sketch in sketches:
                s = ""
                for x in range(0, rows):
                    s += sketch[b * rows + x]
                if s in buckets:
                    buckets[s].append(e)
                else:
                    buckets[s] = [e]
            for k in buckets:
                for pair in itertools.combinations(buckets[k], 2):
                    if (pair[1], pair[0]) not in self._pairs:
                        pairs.add(pair)

        self._pairs = iter(pairs)

    def next(self):
        return self._pairs.next()
