__author__ = 'Francesco Infante'

from api import Feature


class OverlapCoefficient(Feature):
    def extract(self, x, y):
        if x is None or y is None:
            return 0
        x = set(x)
        y = set(y)
        return float(len(x & y)) / min(len(x), len(y))


class DiceCoefficient(Feature):
    def extract(self, x, y):
        # TODO
        raise NotImplementedError()


class JaccardIndex(Feature):
    def extract(self, x, y):
        if x is None or y is None:
            return 0
        x = set(x)
        y = set(y)
        return float(len(x & y)) / len(x | y)
