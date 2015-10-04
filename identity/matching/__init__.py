__author__ = 'Francesco Infante'

from fellegi_sunter import FellegiSunter
from weighted_sum import WeightedSum
from sklearn_classifier import SklearnClassifier

if __name__ == "__main__":
    sample = {'ExactMatch@year': 1,
              'Levenshtein@title': 0.6,
              'MongeElkan@genre': 0.9805555555555556,
              'JaccardIndex@actors': 0.3333333333333333}

    conf = {'ExactMatch@year': 1,
            'Levenshtein@title': 1,
            'MongeElkan@genre': 1,
            'JaccardIndex@actors': 1}

    print WeightedSum(conf, thresholds=[(0, 0.0), (1, 3)]).predict(sample)
