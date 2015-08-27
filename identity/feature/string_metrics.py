__author__ = 'Francesco Infante'

from jellyfish import levenshtein_distance

from api import Feature


class Levenshtein(Feature):
    def extract(self, x, y):
        return levenshtein_distance(unicode(x), unicode(y))


class WeightedLevenshtein(Feature):
    pass

class DamerauLevenshtein(Feature):
    pass


class SmithWaterman(Feature):
    pass



class Jaro(Feature):
    pass

class JaroWinkler(Feature):
    pass


class MongeElkane(Feature):
    pass



class AffineGapDistance(Feature):
    pass





