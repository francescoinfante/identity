__author__ = 'Francesco Infante'


class Feature(object):
    def prefix(self):
        raise NotImplementedError()

    def extract(self, pair):
        raise NotImplementedError()
