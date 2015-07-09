__author__ = 'Francesco Infante'

from api import Transformation


class ConfigTransform(Transformation):
    """
    Apply the configuration to each entry of the source
    """

    def __init__(self, source, config):
        self.source = source
        self.config = config

    def transform(self, data):
        # TODO
        pass

    def next(self):
        return self.transform(self.source.next())
