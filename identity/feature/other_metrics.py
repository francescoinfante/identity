__author__ = 'Francesco Infante'

from api import Feature


class ExactComparator(Feature):
    def extract(self, x, y):
        return 1 if x == y else 0


class GeopositionComparator(Feature):
    "latitute and longitude"
    pass


class NumericComparatorRelative(Feature):
    "ratio smaller/bigger"
    pass


class NumericComparatorAbsolute(Feature):
    "ratio smaller/bigger"
    pass


class LongestCommonSubsequence(Feature):
    pass


class DateDistance(Feature):
    pass
