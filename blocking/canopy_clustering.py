__author__ = 'Francesco Infante'

from api import Blocking


class CanopyClustering(Blocking):
    """
    Algorithm based on McCallum et al. (2000).

    It takes as arguments the documents, the distance metric (instance of Feature) and the thresholds t1 and t2.

    The distance metric must give a numeric value.

    It returns all the pairs within a canopy (Non-disjoint blocking).
    """

    def __init__(self, source, distance, t1, t2):

    # TODO

    def next(self):
        return self._pairs.next()
