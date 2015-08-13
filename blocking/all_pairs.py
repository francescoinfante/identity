__author__ = 'Francesco Infante'

from itertools import combinations

from api import Blocking


class AllPairs(Blocking):
    def __init__(self, pairs):
        self.pairs = combinations(pairs, 2)

    def next(self):
        return self.pairs.next()
