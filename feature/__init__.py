__author__ = 'Francesco Infante'


class FeaturesExtraction(object):
    def __init__(self, pairs, features):
        self.pairs = pairs
        self.features = features

    def next(self):
        pair = self.pairs.next()
        features_vector = {}
        for feat in self.features:
            result = feat.extract(pair)
            if isinstance(result, dict):
                features_vector.update({feat.prefix() + ':' + str(name): value for name, value in result.iteritems()})
            else:
                features_vector[feat.prefix()] = result
        return features_vector
