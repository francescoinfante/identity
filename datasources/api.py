__author__ = 'Francesco Infante'


class Source(object):
    def next(self):
        raise NotImplementedError()

    def __iter__(self):
        return self
