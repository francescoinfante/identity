__author__ = 'Francesco Infante'

from collections import Counter
import logging
import math

from api import DataMatching

logger = logging.getLogger(__name__)


class FellegiSunter(DataMatching):
    def __init__(self, training_set):
        self.count_white = Counter()
        self.count_black = Counter()
        self.tot_white = 0
        self.tot_black = 0

        for x, t in training_set:
            if t == 1:
                self.tot_white += 1
            else:
                self.tot_black += 1
            for k, v in x.iteritems():
                if t == 1:
                    self.count_white[k + ':' + str(v)] += 1
                else:
                    self.count_black[k + ':' + str(v)] += 1

    def predict(self, comparison_vector):
        score = 0.0
        for k, v in comparison_vector.iteritems():
            key = k + ':' + str(v)

            if self.count_white[key] > 0 and self.count_black[key] > 0:
                score += math.log((float(self.count_white[key]) / self.tot_white) /
                                  (float(self.count_black[key]) / self.tot_black), 2)
            elif self.count_white[key] > 0:
                score = float("inf")
                break
            else:
                score = float("-inf")
                break

        # TODO add manual thresholds and/or automatic thresholds and return class

        return score
