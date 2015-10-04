__author__ = 'Francesco Infante'

from sklearn.externals import joblib
import os.path
from api import DataMatching


class SklearnClassifier(DataMatching):
    def __init__(self, classifier=None, training_set=None, model_path=None):
        if model_path is not None and os.path.exists(model_path):
            self.classifier = joblib.load(model_path)
        else:
            self.classifier = classifier

            keys = sorted(training_set[0][0].keys())

            X = [[x[k] for k in keys] for x, _ in training_set]
            y = [y for _, y in training_set]

            self.classifier.fit(X, y)

        if model_path is not None and not os.path.exists(model_path):
            joblib.dump(self.classifier, model_path)

    def predict(self, comparison_vector):
        keys = sorted(comparison_vector.keys())
        comparison_vector = [comparison_vector[k] for k in keys]
        return self.classifier.predict(comparison_vector)[0]
