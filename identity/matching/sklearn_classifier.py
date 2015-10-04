__author__ = 'Francesco Infante'

from sklearn.externals import joblib

from api import DataMatching


class SklearnClassifier(DataMatching):
    def __init__(self, classifier=None, training_set=None, load_model_from=None, save_model_to=None):
        if load_model_from is not None:
            self.classifier = joblib.load(load_model_from)
        else:
            self.classifier = classifier

            keys = sorted(training_set[0].keys())

            X = [[x[k] for k in keys] for x, _ in training_set]
            y = [y for _, y in training_set]

            self.classifier.fit(X, y)

        if save_model_to is not None:
            joblib.dump(self.classifier, save_model_to)

    def predict(self, comparison_vector):
        keys = sorted(comparison_vector.keys())
        comparison_vector = [comparison_vector[k] for k in keys]
        return self.classifier.predict(comparison_vector)[0]
