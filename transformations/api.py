__author__ = 'Francesco Infante'


class Transformation(object):
    def next(self):
        raise NotImplementedError()

    def __iter__(self):
        return self
