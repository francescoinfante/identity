__author__ = 'Francesco Infante'

import re
from itertools import izip, repeat

from unidecode import unidecode
from jellyfish import soundex, metaphone, nysiis, match_rating_codex

from dateutil import parser as dateparse

from dpath import util

from api import Transformation
from identity.common import Path


def transform(args):
    data = args[0]
    config = args[1]

    result = config
    if isinstance(config, dict):
        result = {k: transform((data, v)) for k, v in config.iteritems()}
    elif isinstance(config, Transformation):
        args = [transform((data, v)) for v in config.args]
        kwargs = {k: transform((data, v)) for k, v in config.kwargs.iteritems()}
        result = config.transform(*args, **kwargs)
    elif isinstance(config, Map):
        result = config.get_result(transform((data, config.source)))
    elif isinstance(config, Path):
        try:
            if config == '' or config == '/':
                result = data
            else:
                result = util.get(data, config)
        except:
            result = None

    if isinstance(result, list):
        result = [x for x in result if x is not None]

    if isinstance(result, dict):
        result = {k: v for k, v in result.iteritems() if v is not None}

    return result


class Map(object):
    """
    Args:
        source (list): list of data
        config (Configuration or Transformation): apply the configuration or the transformation to each element in input
    """

    def __init__(self, source, config):
        self.source = source
        self.config = config

    def get_result(self, source):
        if hasattr(source, '__iter__'):
            return map(transform, izip(source, repeat(self.config)))


class Apply(Transformation):
    def __init__(self, function, *args, **kwargs):
        super(Apply, self).__init__(*args, **kwargs)
        self.function = function

    def transform(self, *args, **kwargs):
        try:
            return self.function(*args, **kwargs)
        except:
            pass


class DigitsOnly(Transformation):
    def transform(self, data, convert=False):
        if isinstance(data, basestring):
            data = re.sub('[^0-9]', '', str(data))
            if len(data) > 0:
                if convert:
                    return int(data)
                else:
                    return data


class LowerCase(Transformation):
    def transform(self, data):
        """
        Lowercase all the letters and remove accents, whitespaces to both ends and multiple consecutive whitespaces.

        Args:
            data (basestring)

        Returns:
            str
        """
        if isinstance(data, basestring):
            if isinstance(data, unicode):
                data = unidecode(data)
            data = re.sub(' +', ' ', data.lower().strip())
            if len(data) > 0:
                return data


class NGram(Transformation):
    def transform(self, data, size):
        if isinstance(data, basestring):
            data = LowerCase().transform(data).split()
            ngrams = []
            for x in range(0, len(data) - size + 1):
                ngrams.append(data[x:x + size])
            return ngrams


class QGram(Transformation):
    def transform(self, data, size):
        if isinstance(data, basestring):
            data = LowerCase().transform(data)
            qgrams = []
            for x in range(0, len(data) - size + 1):
                qgrams.append(data[x:x + size])
            return qgrams


class ParseDate(Transformation):
    def transform(self, data, dayfirst=False):
        if isinstance(data, basestring):
            return dateparse.parse(data, fuzzy=True, dayfirst=dayfirst)


class PyParse(Transformation):
    """
    Pyparsing wrapper.
    """

    def transform(self, grammar, data):
        if isinstance(data, basestring):
            return grammar.parseString(data)


"""
Phonetic encoding
"""


class Soundex(Transformation):
    def transform(self, data):
        if isinstance(data, basestring):
            return soundex(unicode(data))


class Metaphone(Transformation):
    def transform(self, data):
        if isinstance(data, basestring):
            return metaphone(unicode(data))


class NYSIIS(Transformation):
    def transform(self, data):
        if isinstance(data, basestring):
            return nysiis(unicode(data))


class MatchRatingApproach(Transformation):
    def transform(self, data):
        if isinstance(data, basestring):
            return match_rating_codex(unicode(data))
