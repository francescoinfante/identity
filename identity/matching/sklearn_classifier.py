__author__ = 'Francesco Infante'

import os.path
import logging

from sklearn.externals import joblib
from sklearn import cross_validation

from api import DataMatching

logger = logging.getLogger(__name__)


class SklearnClassifier(DataMatching):
    def __init__(self, classifier=None, training_set=None, model_path=None, validate=False, validate_times=10):
        if model_path is not None and os.path.exists(model_path) and not validate:
            logger.info('loading model from dump file')
            self.classifier = joblib.load(model_path)
        else:
            self.classifier = classifier

            keys = sorted(training_set[0][0].keys())

            X = [[x[k] for k in keys] for x, _ in training_set]
            y = [y for _, y in training_set]

            self.validate = validate
            if validate:
                scores = cross_validation.cross_val_score(classifier, X, y, validate_times)
                logger.info('Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std() * 2))
            else:
                self.classifier.fit(X, y)

        if model_path is not None and not os.path.exists(model_path) and not validate:
            logger.info('saving model to dump file')
            joblib.dump(self.classifier, model_path)

    def predict(self, comparison_vector):
        if self.validate:
            logger.info('validate was set to True')
            return None
        keys = sorted(comparison_vector.keys())
        comparison_vector = [comparison_vector[k] for k in keys]
        return self.classifier.predict(comparison_vector)[0]
