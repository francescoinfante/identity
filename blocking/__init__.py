__author__ = 'Francesco Infante'

from all_pairs import AllPairs
from canopy_clustering import CanopyClustering
from min_hash import MinHash
from sorted_neighborhood import SortedNeighborhood
from conjunction_of_attributes import ConjunctionOfAttributes
from api import Blocking
from common import extract_from_tuple


class MultipleBlocking(Blocking):
    """
    Args:
        blocking_algorithms (list(Blocking)): list of blocking algorithms
    """

    def __init__(self, blocking_algorithms):
        self._blocking_algorithms = blocking_algorithms
        self._current = 0

    def next(self):
        if self._current >= len(self._blocking_algorithms):
            raise StopIteration()
        try:
            return self._blocking_algorithms[self._current].next()
        except StopIteration:
            self._current += 1
            return self.next()


class JoinBlocks(object):
    """
    Args:
        blocking_algorithm (Blocking): a blocking algorithm (also a MultipleBlocking)
        unique_attribute (Path): path to the unique attribute (e.g: ID)
    """

    def __init__(self, blocking_algorithm, unique_attribute):
        self._blocking_algorithm = blocking_algorithm
        self._unique_attribute = unique_attribute
        self._consumed = set()
        self._current = None

    def __iter__(self):
        return self

    def next(self):
        if self._current is None:
            self._current = self._blocking_algorithm.next()
        try:
            e = self._current.next()
            u = extract_from_tuple(e, self._unique_attribute)
            if u in self._consumed or (u[1], u[0]) in self._consumed:
                return self.next()
            else:
                self._consumed.add(u)
                return e
        except StopIteration:
            self._current = self._blocking_algorithm.next()
            return self.next()


if __name__ == "__main__":
    sample = [{'test': 1}, {'test': 2}, {'test': 3}, {'test': 4}, {'test': 5}]
    sample_2 = [{'test': 2}, {'test': 1}, {'test': 3}]

    mb = MultipleBlocking([AllPairs(sample), AllPairs(sample_2)])

    for x in JoinBlocks(mb, 'test'):
        print x
