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
    elif isinstance(config, ApplyConf):
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
        if len(result) > 0:
            return result
    elif isinstance(result, dict):
        result = {k: v for k, v in result.iteritems() if v is not None}
        if len(result) > 0:
            return result
    else:
        return result


class Map(object):
    """
    Args:
        source (list): list of data
        config (Configuration or Transformation): apply the configuration or the transformation to each element
    """

    def __init__(self, source, config, no_duplicate=False, no_none=False):
        self.source = source
        self.config = config
        self.no_none = no_none
        self.no_duplicate = no_duplicate

    def get_result(self, source):
        if hasattr(source, '__iter__'):
            result = map(transform, izip(source, repeat(self.config)))
            if self.no_none or self.no_duplicate:
                result = [x for x in result if x is not None]
            if self.no_duplicate:
                result = list(set(result))
            return result


class ApplyConf(object):
    def __init__(self, source, config):
        self.source = source
        self.config = config

    def get_result(self, source):
        if source is not None:
            return transform((source, self.config))


class Apply(Transformation):
    def __init__(self, function, *args, **kwargs):
        super(Apply, self).__init__(*args, **kwargs)
        self.function = function

    def transform(self, *args, **kwargs):
        try:
            return self.function(*args, **kwargs)
        except:
            pass


class Chain(Transformation):
    def transform(self, *args):
        result = set()
        for x in args:
            if x is not None:
                if isinstance(x, list):
                    for y in x:
                        result.add(y)
                else:
                    result.add(x)
        if len(result) > 0:
            return list(result)


class Or(Transformation):
    def transform(self, *args):
        for x in args:
            if x is not None:
                return x


class And(Transformation):
    def transform(self, *args):
        if len(args) >= 1:
            t = args[0]
            for x in args:
                if x != t:
                    return None
            return t


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
    def transform(self, data, fuzzy=False, dayfirst=False):
        if isinstance(data, basestring):
            return dateparse.parse(data, fuzzy=fuzzy, dayfirst=dayfirst)


class ParseMonth(Transformation):
    def transform(self, data):
        if isinstance(data, basestring):
            try:
                v = int(data)
                if 1 <= v <= 12:
                    return v
            except:
                pass
            try:
                return dateparse.parse(data, fuzzy=False).month
            except:
                pass


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
