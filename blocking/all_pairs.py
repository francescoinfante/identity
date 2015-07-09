__author__ = 'Francesco Infante'

from itertools import combinations

from api import Block


class AllPairs(Block):
    def __init__(self, source):
        self.pairs = combinations(source, 2)

    def next(self):
        return self.pairs.next()
