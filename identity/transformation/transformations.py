__author__ = 'Francesco Infante'

import re

from unidecode import unidecode


def lower_case(data):
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


def digits_only(data):
    """
    Remove everything which is not a digit.
    """
    return re.sub('[^0-9]', '', data)


def phone_number():
    raise NotImplementedError()


def person_name():
    raise NotImplementedError()

def date():
    raise NotImplementedError()

def cities():
    raise NotImplementedError()


def generic_value_cleaner():
    """
    Remove value too common that probably represents a None
    """
    raise NotImplementedError()


def shingles():
    raise NotImplementedError()

def ngram():
    raise NotImplementedError()

def qgram():
    raise NotImplementedError()

def reference_table():
    raise NotImplementedError()


def regexp_cleaner():
    """
    Returns the part matching the group
    """
    raise NotImplementedError()

def soundex():
    pass

def metaphone():
    pass


