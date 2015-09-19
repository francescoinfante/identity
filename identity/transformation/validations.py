__author__ = 'Francesco Infante'

from stdnum import issn, isbn

from api import Transformation


class MinLength(Transformation):
    def transform(self, data, length):
        if hasattr(data, '__len__'):
            return data if len(data) >= length else None


class MaxLength(Transformation):
    def transform(self, data, length):
        if hasattr(data, '__len__'):
            return data if len(data) <= length else None


class ValidRange(Transformation):
    def transform(self, data, lower, upper):
        return data if lower <= data <= upper else None


class ValidISSN(Transformation):
    def transform(self, data):
        try:
            return issn.validate(data)
        except:
            pass


class ValidISBN(Transformation):
    def transform(self, data):
        try:
            return isbn.validate(data, convert=True)
        except:
            pass
