__author__ = 'Francesco Infante'

from jellyfish import levenshtein_distance

from api import Feature


class Levenshtein(Feature):
    def extract(self, x, y):
        return levenshtein_distance(unicode(x), unicode(y))
