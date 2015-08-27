__author__ = 'Francesco Infante'

from api import Feature




class ExactComparator(Feature):
    "1 match 0 no"
    pass

class GeopositionComparator(Feature):
    "latitute and longitude"
    pass

class NumericComparatorRelative(Feature):
    "ratio smaller/bigger"
    pass

class NumericComparatorAbsolute(Feature):
    "ratio smaller/bigger"
    pass


class HammingDistance(Feature):
    pass



class LongestCommonSubsequence(Feature):
    pass


class DateDistance(Feature):
    pass
