__author__ = 'Francesco Infante'

import ujson

from api import DataSource


class JSONSource(DataSource):
    """
    Read from a file where each line is a document represented as a JSON object
    """

    def __init__(self, filename):
        self.file = open(filename)

    def next(self):
        return ujson.loads(self.file.next())
