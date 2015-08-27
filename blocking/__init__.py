__author__ = 'Francesco Infante'

from all_pairs import AllPairs
from canopy_clustering import CanopyClustering
from min_hash import MinHash
from sorted_neighborhood import SortedNeighborhood
from conjunction_of_attributes import ConjunctionOfAttributes
from multiple_blocking import MultipleBlocking
from api import Blocking
from common import extract_from_tuple


class JoinBlocks(object):
    """
    Args:
        blocking_algorithm (Blocking): blocking algorithm
        unique_attribute (Path): path to the unique attribute (e.g. ID)
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
    sample = [{'key': 1, 'set_attr': {1, 2, 3}},
              {'key': 2, 'set_attr': {1, 2, 3}, 'year': 2015},
              {'key': 3, 'set_attr': {1, 2, 4}, 'year': 2015}]

    print 'Conjunction of attributes:'

    for x in JoinBlocks(ConjunctionOfAttributes(sample, ['year']), 'key'):
        print x

    print 'MinHash:'

    for x in JoinBlocks(MinHash(sample, 'set_attr', 2, 2), 'key'):
        print x

    print 'Both:'

    mb = MultipleBlocking([ConjunctionOfAttributes(sample, ['year']), MinHash(sample, 'set_attr', 2, 2)])

    for x in JoinBlocks(mb, 'key'):
        print x
