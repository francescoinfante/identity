__author__ = 'Francesco Infante'

from inspect import isclass

from string_metrics import Hamming, Levenshtein, DamerauLevenshtein, Jaro, JaroWinkler, AffineGapDistance, \
    SmithWaterman, MongeElkan
from other_metrics import ExactMatch
from set_metrics import JaccardIndex
from identity.common import extract_from_tuple, Path


class FeatureExtraction(object):
    """
    Args:
        source ([tuple]): list of pairs of records
        features ([(Feature, Path)]): list of features to extract from each pair from the given path
    """

    def __init__(self, pairs, features):
        self.pairs = iter(pairs)
        self.features = features

    def __iter__(self):
        return self

    def next(self):
        pair = self.pairs.next()
        features_vector = {}
        for feat, path in self.features:
            if isclass(feat):
                feat = feat()
            e = extract_from_tuple(pair, path)
            result = feat.extract(e[0], e[1])
            if isinstance(result, dict):
                features_vector.update({feat.__class__.__name__ + '@' + path + ':' + str(name): value for name, value in
                                        result.iteritems()})
            else:
                features_vector[feat.__class__.__name__ + '@' + path] = result
        return features_vector


if __name__ == "__main__":
    sample = [({'id': 3, 'title': 'matrix',
                'year': 1999,
                'actors': ['keanu reeves', 'laurence fishburne'],
                'genre': 'scifi action'},
               {'id': 5, 'title': 'the matrix',
                'year': 1999,
                'actors': ['keanu reeves', 'carrie-anne moss'],
                'genre': 'action sci-fi'})]

    feats = [(Levenshtein(True), Path('title')), (ExactMatch, Path('year')), (JaccardIndex, Path('actors')),
             (MongeElkan, Path('genre'))]

    for x in FeatureExtraction(sample, feats):
        print x
