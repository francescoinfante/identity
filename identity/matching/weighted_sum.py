__author__ = 'Francesco Infante'

from api import DataMatching


class WeightedSum(DataMatching):
    def __init__(self, configuration, thresholds=((0, 0.0), (1, 0.5))):
        self.configuration = configuration
        self.thresholds = sorted(list(thresholds), key=lambda x: x[1], reverse=True)

    def predict(self, comparison_vector):
        score = 0.0
        print self.configuration
        for k, v in self.configuration.iteritems():
            score += float(v) * float(comparison_vector[k])

        for n, t in self.thresholds:
            if score >= t:
                return n
