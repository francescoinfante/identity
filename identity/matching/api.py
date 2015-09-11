__author__ = 'Francesco Infante'


class DataMatching(object):
    def next(self):
        raise NotImplementedError()

    def __iter__(self):
        return self
