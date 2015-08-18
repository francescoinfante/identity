__author__ = 'Francesco Infante'

from api import Blocking


class MultipleBlocking(Blocking):
    """
    Args:
        blocking_algorithms (list(Blocking)): list of blocking algorithms
    """

    def __init__(self, blocking_algorithms):
        self._blocking_algorithms = blocking_algorithms
        self._current = 0

    def next(self):
        if self._current >= len(self._blocking_algorithms):
            raise StopIteration()
        try:
            return self._blocking_algorithms[self._current].next()
        except StopIteration:
            self._current += 1
            return self.next()
