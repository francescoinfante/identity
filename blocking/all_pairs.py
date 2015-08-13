__author__ = 'Francesco Infante'

from itertools import combinations

from api import Blocking


class AllPairs(Blocking):
    """
    It returns all the possible combinations.
    """

    def __init__(self, source):
        self._pairs = combinations(source, 2)

    def next(self):
        return self._pairs.next()
