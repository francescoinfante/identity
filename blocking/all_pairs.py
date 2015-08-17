__author__ = 'Francesco Infante'

from itertools import combinations

from api import Blocking


class AllPairs(Blocking):
    def __init__(self, source):
        self._blocks = iter([combinations(source, 2)])

    def next(self):
        return self._blocks.next()
