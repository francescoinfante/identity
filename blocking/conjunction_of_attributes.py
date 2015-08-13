__author__ = 'Francesco Infante'

import itertools

import dpath.util

from api import Blocking


class ConjunctionOfAttributes(Blocking):
    """
    It takes as arguments the documents and a list of attributes (instances of Path).
    Attributes must be hashables.
    It hashes the conjunction of attributes of each document and put the document in the bucket for that hash.
    It returns all the pairs within a bucket (Disjoint blocking).
    """

    def __init__(self, source, attributes):
        buckets = {}
        for e in source:
            tmp = []
            for a in attributes:
                tmp.append(dpath.util.get(e, a.path))
            h = hash(tuple(tmp))
            if h in buckets:
                buckets[h].append(e)
            else:
                buckets[h] = [e]

        self._pairs = itertools.chain(*[v for _, v in buckets.iteritems()])

    def next(self):
        return self._pairs.next()
