__author__ = 'Francesco Infante'

import logging

from all_pairs import AllPairs
from canopy_clustering import CanopyClustering
from min_hash import MinHash
from sorted_neighborhood import SortedNeighborhood
from conjunction_of_attributes import ConjunctionOfAttributes
from multiple_blocking import MultipleBlocking
from api import Blocking
from identity.common import extract_from_tuple

logger = logging.getLogger(__name__)


class JoinBlocks(object):
    """
    Args:
        blocking_algorithm (Blocking): blocking algorithm
        unique_attribute (Path): path to the unique attribute (e.g. ID)
    """

    def __init__(self, blocking_algorithm, unique_attribute, debug=False):
        self._consumed = set()

        count = 0

        if debug:
            logger.info('joinblock start')

        for x in blocking_algorithm:
            for y in x:

                count += 1

                if debug and count % 1000 == 0:
                    logger.info('tick ' + str(count))

                u = extract_from_tuple(y, unique_attribute)
                self._consumed.add(tuple(sorted(u)))

        if debug:
            logger.info('joinblock done')

    def __iter__(self):
        return iter(list(self._consumes))


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
