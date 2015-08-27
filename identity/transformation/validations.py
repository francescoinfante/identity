__author__ = 'Francesco Infante'

from api import Transformation


class MinLength(Transformation):
    def transform(self, data, length):
        return data if len(data) >= length else None


class MaxLength(Transformation):
    def transform(self, data, length):
        return data if len(data) <= length else None


class ValidRange(Transformation):
    def transform(self, data, lower, upper):
        return data if lower <= data <= upper else None
