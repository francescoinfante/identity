__author__ = 'Francesco Infante'


class Transformation(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def transform(self, *arg, **kwargs):
        raise NotImplementedError()
