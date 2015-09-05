__author__ = 'Francesco Infante'

from scipy.spatial import distance

from api import Feature


class CosineSimilarity(Feature):
    def extract(self, x, y):
        if x is None or y is None or len(x) != len(y) or x.count(0) == len(x) or y.count(0) == len(y):
            return 0
        return distance.cosine(x, y)


class EuclideanDistance(Feature):
    def extract(self, x, y):
        if x is None or y is None or len(x) != len(y):
            return 0
        return distance.euclidean(x, y)
