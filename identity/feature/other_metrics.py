__author__ = 'Francesco Infante'

from api import Feature


class Apply(Feature):
    def __init__(self, function, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.function = function

    def extract(self, x, y):
        return self.function(x, y, *self.args, **self.kwargs)


class ExactMatch(Feature):
    def extract(self, x, y):
        return 1 if x == y else 0

"""
class ContainsWord(Feature):
    def __init__(self, training_set, path):
        for x,_ in training_set:
            try
            (util.get(x, path))
        except:
            result.append(None)

    def extract(self, x, y):
        pass
"""