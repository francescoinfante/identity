__author__ = 'Francesco Infante'

import multiprocessing
from multiprocessing import Pool
from itertools import izip, repeat

from common import Configuration, extract_from_tuple
from conflict_resolution_functions import Min, Max, Sum, Count, Avg, Random, Longest, Shortest, Choose, Vote, Group, \
    Escalate


def _merge_records(args):
    data = args[0]
    config = args[1]

    if len(data) == 1:
        return data[0]

    result = {}

    for k, v in config.iteritems():
        if isinstance(v, dict):
            result[k] = _merge_records((extract_from_tuple(data, k), v))
        elif isinstance(v, tuple):
            for x in v:
                result[k] = x.resolve(extract_from_tuple(data, k), data)
                if result[k] is not None:
                    break
        else:
            result[k] = v.resolve(extract_from_tuple(data, k), data)

    return result


class DataFusion(object):
    """
    Args:
        source ([tuple]): each tuple contains the records to merge
        config (Configuration): configuration to apply to each tuple
    """

    def __init__(self, source, config, processes=multiprocessing.cpu_count()):
        self._pool = Pool(processes)
        self._results = self._pool.imap(_merge_records, izip(source, repeat(config)))

    def __iter__(self):
        return self

    def next(self):
        return self._results.next()

    def __del__(self):
        self._pool.close()


if __name__ == "__main__":
    test_sample = [({'title': 'V per vendetta', 'year': 2005, 'director': 'James McTeigue'},
                    {'title': 'V for vendetta', 'director': 'J. McTeigue'}),
                   ({'title': 'Maatrix', 'year': 1999, 'director': 'The Wachowskis',
                     'actors': ['Keanu Reeves', 'Carrie-Anne Moss']},
                    {'title': 'The Matrix', 'year': 1998, 'director': 'The Wachowskis',
                     'actors': ['Keanu Reeves', 'Laurence Fishburne']},
                    {'title': 'Matrix', 'director': 'Wachowski Brothers'})]

    c = Configuration(title=(Vote(), Longest()), director=(Vote(), Longest()), year=(Vote(), Random()), actors=Group())

    for i in DataFusion(test_sample, c):
        print i
