__author__ = 'Francesco Infante'

from random import choice
from collections import Counter
from itertools import combinations

from api import ConflictResolutionFunction
from common import extract_from_tuple


class Min(ConflictResolutionFunction):
    def resolve(self, data, _):
        data = [x for x in data if x is not None]
        if len(data) > 0:
            return min(data)


class Max(ConflictResolutionFunction):
    def resolve(self, data, _):
        data = [x for x in data if x is not None]
        if len(data) > 0:
            return max(data)


class Sum(ConflictResolutionFunction):
    def resolve(self, data, _):
        return sum([x for x in data if x is not None])


class Count(ConflictResolutionFunction):
    def resolve(self, data, _):
        return len(data) - data.count(None)


class Avg(ConflictResolutionFunction):
    def resolve(self, data, _):
        s = sum([x for x in data if x is not None])
        c = len(data) - data.count(None)
        if c > 0:
            return float(s) / c


class Random(ConflictResolutionFunction):
    def resolve(self, data, _):
        data = [x for x in data if x is not None]
        if len(data) > 0:
            return choice(data)


class Longest(ConflictResolutionFunction):
    def resolve(self, data, _):
        data = [x for x in data if x is not None]
        if len(data) > 0:
            t = data[0]
            for x in data:
                if len(x) > len(t):
                    t = x
            return t


class Shortest(ConflictResolutionFunction):
    def resolve(self, data, _):
        data = [x for x in data if x is not None]
        if len(data) > 0:
            t = data[0]
            for x in data:
                if len(x) < len(t):
                    t = x
            return t


class Choose(ConflictResolutionFunction):
    def __init__(self, source_field, source_value):
        self._source_field = source_field
        self._source_value = source_value

    def resolve(self, conflict_data, all_data):
        sources = extract_from_tuple(all_data, self._source_field)
        for x in range(0, len(sources)):
            if sources[x] == self._source_value:
                return conflict_data[x]


class Vote(ConflictResolutionFunction):
    def resolve(self, data, _):
        data = Counter([x for x in data if x is not None]).most_common()
        if len(data) == 1 or (len(data) > 1 and data[0][1] > data[1][1]):
            return data[0][0]


class Group(ConflictResolutionFunction):
    def resolve(self, data, _):
        data = [x for x in data if x is not None]
        r = set()
        for x in data:
            r |= set(x)
        return r


class Escalate(ConflictResolutionFunction):
    def resolve(self, data, _):
        data = [x for x in data if x is not None]
        r = tuple(set(data))
        if len(r) == 1:
            return r[0]
        if len(r) > 1:
            return r


class MostRecent(ConflictResolutionFunction):
    def __init__(self, date_field):
        self._date_field = date_field

    def resolve(self, conflict_data, all_data):
        dates = extract_from_tuple(all_data, self._date_field)
        result = conflict_data[0]
        last_date = dates[0]
        for x in range(0, len(dates)):
            if dates[x] > last_date and conflict_data[x] is not None:
                result = conflict_data[x]
                last_date = dates[x]
        return result


class HighestAverageSimilarity(ConflictResolutionFunction):
    def __init__(self, similarity_metric, distance=False):
        self.similarity_metric = similarity_metric
        self.distance = distance

    def resolve(self, data, _):
        data = [x for x in data if x is not None]
        if len(data) == 1:
            return data[0]
        if len(data) > 1:
            averages = Counter()

            for x, y in combinations(data, 2):
                similarity = self.similarity_metric.extract(x, y)
                averages[x] += similarity
                averages[y] += similarity

            most_common = averages.most_common()
            if self.distance:
                return most_common[-1][0]
            else:
                return most_common[0][0]
