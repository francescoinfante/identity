__author__ = 'Francesco Infante'

from jellyfish import levenshtein_distance, damerau_levenshtein_distance, jaro_distance, jaro_winkler, hamming_distance

from api import Feature


class Hamming(Feature):
    def __init__(self, similarity=False):
        self.similarity = similarity

    def extract(self, x, y):
        if x is None or y is None:
            return 0
        if self.similarity:
            return 1 - float(hamming_distance(unicode(x), unicode(y))) / max(len(x), len(y))
        else:
            return hamming_distance(unicode(x), unicode(y))


class Levenshtein(Feature):
    def __init__(self, similarity=False):
        self.similarity = similarity

    def extract(self, x, y):
        if x is None or y is None:
            return 0
        if self.similarity:
            return 1 - float(levenshtein_distance(unicode(x), unicode(y))) / max(len(x), len(y))
        else:
            return levenshtein_distance(unicode(x), unicode(y))


class DamerauLevenshtein(Feature):
    def __init__(self, similarity=False):
        self.similarity = similarity

    def extract(self, x, y):
        if x is None or y is None:
            return 0
        if self.similarity:
            return 1 - float(damerau_levenshtein_distance(unicode(x), unicode(y))) / max(len(x), len(y))
        else:
            return damerau_levenshtein_distance(unicode(x), unicode(y))


class Jaro(Feature):
    def extract(self, x, y):
        if x is None or y is None:
            return 0
        return jaro_distance(unicode(x), unicode(y))


class JaroWinkler(Feature):
    def extract(self, x, y):
        if x is None or y is None:
            return 0
        return jaro_winkler(unicode(x), unicode(y))


class AffineGap(Feature):
    def extract(self, x, y):
        # TODO
        raise NotImplementedError()


class MongeElkan(Feature):
    def extract(self, x, y):
        if x is None or y is None:
            return 0
        if isinstance(x, list):
            toks_x = x
            toks_y = y
        else:
            toks_x = x.split()
            toks_y = y.split()

        if len(toks_x) > len(toks_y):
            toks_x, toks_y = toks_y, toks_x

        sum = 0.0

        for x in toks_x:
            best_x = 0.0
            for y in toks_y:
                best_x = max(best_x, JaroWinkler().extract(x, y))
            sum += best_x

        return sum / min(len(toks_x), len(toks_y))
