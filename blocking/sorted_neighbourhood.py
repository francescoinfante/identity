__author__ = 'Francesco Infante'

import dpath.util

from api import Blocking


class SortedNeighbourhood(Blocking):
    """
    Algorithm based on Hernandez and Stolfo (1995).

    It takes as arguments the documents, the attribute with the key (instance of Path) and the window size.

    It returns all the pairs within a window (Non-disjoint blocking).
    """

    def __init__(self, source, attribute, window_size):
        l = []
        for e in source:
            key = dpath.util.get(e, attribute.path)
            l.append((key, e))
        self._ordered_list = sorted(l)
        self._window_size = window_size
        self._current_min = 0
        self._current_max = 0

    def next(self):
        if self._current_min >= len(self._ordered_list):
            raise StopIteration()
        if self._current_max >= len(self._ordered_list):
            self._current_min += 1
            self._current_max = self._current_min + 1
            return self.next()
        return self._ordered_list[self._current_min][1], self._ordered_list[self._current_max][1]
