__author__ = 'Francesco Infante'

from sklearn.externals import joblib

from api import Classifier


class SklearnClassifier(Classifier):
    def __init__(self, classifier=None, training_set=None, load_model_from=None, save_model_to=None):
        if load_model_from is not None:
            self.classifier = joblib.load(load_model_from)
        else:
            self.classifier = classifier

            keys = sorted(training_set[0][0])

            X = [[x[k] for k in keys] for x, _ in training_set]
            y = [y for _, y in training_set]

            self.classifier.fit(X, y)

        if save_model_to is not None:
            joblib.dump(self.classifier, save_model_to)

    def predict(self, ):
        return self.classifier.predict()
