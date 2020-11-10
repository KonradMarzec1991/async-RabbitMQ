"""
Module with db models
"""
import numbers


class Pair:
    """
    Base class representing key-value relation
    """
    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key_val):
        if not isinstance(key_val, str):
            raise AttributeError('Key must be a string')
        self._key = key_val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, num):
        if not isinstance(num, numbers.Number):
            raise AttributeError('Value must be a number')
        self._value = num
