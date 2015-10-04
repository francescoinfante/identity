__author__ = 'Francesco Infante'

from collections import Counter
import logging
import math

from api import DataMatching

logger = logging.getLogger(__name__)


def f_score(precision, recall, beta):
    return (1 + beta ** 2) * (precision * recall) / ((beta ** 2) * precision + recall)


def find_best_top_threshold(fs, beta=0.5):
    scores = [(fs.get_score(x), y) for x, y in fs.training_set]

    scores = sorted(scores, key=lambda x: x[0], reverse=True)

    best_top_threshold = 0.0
    best_score = 0

    current_white = 0.0
    current_pos = 1.0

    tot_white = fs.tot_white

    logger.info('finding best top threshold')

    for x, t in scores:
        current_pos += 1
        if t == 1:
            current_white += 1

        current_recall = current_white / tot_white
        current_precision = current_white / current_pos

        current_fscore = f_score(current_precision, current_recall, beta)
        if current_fscore >= best_score:
            best_score = current_fscore
            best_top_threshold = x

    logger.info('threshold found')
    logger.info(best_top_threshold)

    return best_top_threshold


class FellegiSunter(DataMatching):
    def __init__(self, training_set, beta=0.5):
        self.count_white = Counter()
        self.count_black = Counter()
        self.tot_white = 0
        self.tot_black = 0
        self.training_set = training_set

        logger.info('fellegisunter start')

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

        logger.info('counting done')

        self.threshold = find_best_top_threshold(self, beta=beta)

    def get_score(self, comparison_vector):
        score = 0.0
        for k, v in comparison_vector.iteritems():
            key = k + ':' + str(v)

            if self.count_white[key] > 0 and self.count_black[key] > 0:
                score += math.log((float(self.count_white[key]) / self.tot_white) /
                                  (float(self.count_black[key]) / self.tot_black), 2)
            elif self.count_white[key] > 0:
                score = float("inf")
            else:
                score = float("-inf")
                break

        return score

    def predict(self, comparison_vector):
        score = comparison_vector.get_score()
        if score >= self.threshold:
            return 1
        else:
            return 0
