# -*- coding: utf-8 -*-

__author__ = 'Francesco Infante'

from pathos.multiprocessing import Pool, cpu_count
from itertools import izip, repeat

from dpath import util

from identity.common import Configuration, Apply, Path
from api import Transformation
from transformations import LowerCase, DigitsOnly, NGram, QGram, ParseDate, Soundex, Metaphone, NYSIIS, \
    MatchRatingApproach
from validations import MinLength, MaxLength, ValidRange


def _transform(args):
    data = args[0]
    config = args[1]

    result = config
    if isinstance(config, Configuration):
        result = {k: _transform((data, v)) for k, v in config.iteritems()}
    elif isinstance(config, Transformation):
        args = [_transform((data, v)) for v in config.args]
        kwargs = {k: _transform((data, v)) for k, v in config.kwargs.iteritems()}
        result = config.transform(*args, **kwargs)
    elif isinstance(config, Apply):
        args = [_transform((data, v)) for v in config.args]
        kwargs = {k: _transform((data, v)) for k, v in config.kwargs.iteritems()}
        result = config.function(*args, **kwargs)
    elif isinstance(config, Path):
        try:
            result = util.get(data, config)
        except:
            result = None

    return result


class DataTransformation(object):
    """
    Args:
        source ([dict]): list of records
        config (Configuration): configuration to apply to each record
    """

    def __init__(self, source, config, processes=cpu_count()):
        self.pool = Pool(processes)
        self.results = self.pool.imap(_transform, izip(source, repeat(config)))

    def __iter__(self):
        return self

    def next(self):
        return self.results.next()

    def __del__(self):
        self.pool.close()


if __name__ == "__main__":
    sample = [{'_id': 1, 'titolo': u'Matrix', 'year': {'value': 9999},
               'attori': ['Keanu Reeves', 'Laurence Fishburne', 'Carrie-Anne Moss']},
              {'_id': 2, 'titolo': u'V  for Vendetta\n', 'year': {'value': 2005}, 'durata': '132 min'},
              {'_id': 3, 'titolo': u'La vita è bella'}]

    c = Configuration(id=Path('_id'),
                      title=LowerCase(Path('titolo')),
                      year=ValidRange(Path('year/value'), 1000, 2016),
                      length=DigitsOnly(Path('durata'), True),
                      actors=Apply(str.lower, Apply(str, Path('titolo'))))

    for x in DataTransformation(sample, c):
        print x
