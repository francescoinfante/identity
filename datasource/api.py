__author__ = 'Francesco Infante'


class DataSource(object):
    def next(self):
        raise NotImplementedError()

    def __iter__(self):
        return self
