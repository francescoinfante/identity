__author__ = 'Francesco Infante'

import re

from unidecode import unidecode
from jellyfish import soundex, metaphone, nysiis, match_rating_codex
from dateutil import parser as dateparse

from api import Transformation


class LowerCase(Transformation):
    def transform(self, data):
        """
        Lowercase all the letters and remove accents, whitespaces to both ends and multiple consecutive whitespaces.

        Args:
            data (unicode or str)

        Returns:
            str
        """
        if isinstance(data, unicode):
            data = unidecode(data)
        return re.sub(' +', ' ', data.lower().strip())


class DigitsOnly(Transformation):
    def transform(self, data):
        return re.sub('[^0-9]', '', data)


class NGram(Transformation):
    def transform(self, data, size):
        data = data.split()
        ngrams = []
        for x in range(0, len(data) - size + 1):
            ngrams.append(data[x:x + size])
        return ngrams


class QGram(Transformation):
    def transform(self, data, size):
        qgrams = []
        for x in range(0, len(data) - size + 1):
            qgrams.append(data[x:x + size])
        return qgrams


class ParseDate(Transformation):
    def transform(self, data, dayfirst=False):
        return dateparse.parse(data, fuzzy=True, dayfirst=dayfirst)


class PyParse(Transformation):
    def transform(self, grammar, data):
        """
        Pyparsing wrapper.
        """
        return grammar.parseString(data)


"""
Phonetic encoding
"""


class Soundex(Transformation):
    def transform(self, data):
        return soundex(data)


class Metaphone(Transformation):
    def transform(self, data):
        return metaphone(data)


class NYSIIS(Transformation):
    def transform(self, data):
        return nysiis(data)


class MatchRatingApproach(Transformation):
    def transform(self, data):
        return match_rating_codex(data)
