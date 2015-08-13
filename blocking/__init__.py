__author__ = 'Francesco Infante'

from all_pairs import AllPairs
from canopy_clustering import CanopyClustering
from min_hash import MinHash
from sorted_neighbourhood import SortedNeighbourhood
from conjunction_of_attributes import ConjunctionOfAttributes


class MultipleBlocking(object):
    """
    It takes as an argument a list of blocking algorithms (instances of Blocking).
    It returns the union of the results of the single algorithms.
    """

    def __init__(self, blocks):
        self._blocks = blocks
        self._consumed = set()
        self._current = 0

    def next(self):
        if self._current >= len(self._blocks):
            raise StopIteration()
        try:
            e = self._blocks[self._current].next()
            if e in self._consumed or (e[1], e[0]) in self._consumed:
                return self.next()
            self._consumed.add(e)
            return e
        except StopIteration:
            self._current += 1
            return self.next()
