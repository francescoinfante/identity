__author__ = 'Francesco Infante'

from jellyfish import levenshtein_distance, damerau_levenshtein_distance, jaro_distance, jaro_winkler, hamming_distance

from api import Feature


class Levenshtein(Feature):
    def extract(self, x, y):
        return levenshtein_distance(unicode(x), unicode(y))


class DamerauLevenshtein(Feature):
    def extract(self, x, y):
        return damerau_levenshtein_distance(unicode(x), unicode(y))


class Jaro(Feature):
    def extract(self, x, y):
        return jaro_distance(unicode(x), unicode(y))


class JaroWinkler(Feature):
    def extract(self, x, y):
        return jaro_winkler(unicode(x), unicode(y))


class HammingDistance(Feature):
    def extract(self, x, y):
        return hamming_distance(unicode(x), unicode(y))


class WeightedLevenshtein(Feature):
    pass


class SmithWaterman(Feature):
    pass


class MongeElkane(Feature):
    pass


class AffineGapDistance(Feature):
    pass
