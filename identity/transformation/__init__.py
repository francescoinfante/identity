__author__ = 'Francesco Infante'

from itertools import izip, repeat, imap

from pathos.multiprocessing import Pool, cpu_count

from identity.common import Configuration, Path
from api import Transformation
from transformations import transform, Map, Apply, Or, And, LowerCase, DigitsOnly, NGram, QGram, ParseDate, ParseMonth, \
    Soundex, Metaphone, NYSIIS, MatchRatingApproach
from validations import MinLength, MaxLength, ValidRange, ValidISSN, ValidISBN


class DataTransformation(object):
    """
    Args:
        source ([dict]): list of records
        config (Configuration): configuration to apply to each record
    """

    def __init__(self, source, config, single_process=False, processes=cpu_count()):
        if single_process:
            self.results = imap(transform, izip(source, repeat(config)))
        else:
            self.pool = Pool(processes)
            self.results = self.pool.imap(transform, izip(source, repeat(config)))

    def __iter__(self):
        return self

    def next(self):
        return self.results.next()

    def __del__(self):
        try:
            self.pool.close()
        except:
            pass


if __name__ == "__main__":
    sample = [{'imdb_id': 1, 'titolo': u'Matrix', 'year': {'value': 9999},
               'attori': ['Keanu Reeves', 'Laurence Fishburne', 'Carrie-Anne Moss']},
              {'imdb_id': 2, 'titolo': u'V  for Vendetta\n', 'year': {'value': 2005}, 'durata': '132 min'},
              {'imdb_id': 3, 'titolo': u'La vita \xe8 bella',
               'riconoscimenti': [{'type': 'oscar', 'name': 'Miglior film straniero'},
                                  {'type': 'oscar', 'name': 'Miglior attore protagonista'}]}]

    c = Configuration(ids=Configuration(imdb=Path('imdb_id')),
                      title=LowerCase(Path('titolo')),
                      year=ValidRange(Path('year/value'), 1000, 2016),
                      length=DigitsOnly(Path('durata'), True),
                      actors=Map(Path('attori'), LowerCase(Path('/'))),
                      awards=Map(Path('riconoscimenti'),
                                 Configuration(oscar=Apply(lambda x: x == 'oscar', Path('type')),
                                               name=LowerCase(Path('name')))))

    for x in DataTransformation(sample, c):
        print x
