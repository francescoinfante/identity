__author__ = 'Francesco Infante'

from multiprocessing import Pool, cpu_count
from itertools import izip, repeat
from inspect import isclass

from api import ConflictResolutionFunction
from common import extract_from_tuple
from conflict_resolution_functions import Min, Max, Sum, Count, Avg, Random, Longest, Shortest, Choose, Vote, Group, \
    Escalate, MostRecent, HighestAverageSimilarity


def _merge_records(args):
    data = args[0]
    config = args[1]
    if len(args) > 2:
        all_data = args[2]
    else:
        all_data = data

    if len(data) == 1:
        return data[0]

    result = {}

    for k, v in config.iteritems():
        if isinstance(v, dict):
            result[k] = _merge_records((extract_from_tuple(data, k), v, all_data))
        elif isinstance(v, tuple):
            for x in v:
                if isclass(x):
                    x = x()
                result[k] = x.resolve(extract_from_tuple(data, k), all_data)
                if result[k] is not None:
                    break
        else:
            if isclass(v):
                v = v()
            result[k] = v.resolve(extract_from_tuple(data, k), all_data)

    return result


class DataFusion(object):
    """
    Args:
        source ([tuple]): each tuple contains the records to merge
        config (Configuration): configuration to apply to each tuple
    """

    def __init__(self, source, config, processes=cpu_count()):
        self._pool = Pool(processes)
        self._results = self._pool.imap(_merge_records, izip(source, repeat(config)))

    def __iter__(self):
        return self

    def next(self):
        return self._results.next()

    def __del__(self):
        self._pool.close()


if __name__ == "__main__":
    from common import Configuration
    from feature import Levenshtein

    sample = [({'title': 'Maatrix', 'year': 1998, 'director': 'The Wachowskis',
                'actors': ['Keanu Reeves', 'Carrie-Anne Moss']},
               {'source': 'imdb', 'title': 'The Matrix', 'year': 1999,
                'director': 'Wachowskis', 'actors': ['Keanu Reeves']},
               {'title': 'The Matrix', 'year': 1998,
                'director': 'Wachowski Brothers'})]

    c = Configuration(title=(Vote, Longest), director=(Vote, Longest),
                      year=(Choose('source', 'imdb'), Vote, Escalate), actors=Group)

    print DataFusion(sample, c).next()

    sample = [({'title': 'Maatrix'}, {'title': 'Matrix'}, {'title', 'Matrixx'})]

    c = Configuration(title=HighestAverageSimilarity(Levenshtein, distance=True))

    print DataFusion(sample, c).next()
