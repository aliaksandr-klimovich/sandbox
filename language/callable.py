import doctest
from collections.abc import Callable


def f():
    pass


class A:
    pass


class B:
    def __call__(self, *args, **kwargs):
        pass


def main():
    """
    >>> callable(f)
    True
    >>> isinstance(f, Callable)
    True
    >>> callable(A)
    True
    >>> isinstance(A, Callable)
    True
    >>> callable(A())
    False
    >>> isinstance(A(), Callable)
    False
    >>> callable(B)
    True
    >>> isinstance(B, Callable)
    True
    >>> callable(B())
    True
    >>> isinstance(B(), Callable)
    True
    """


doctest.testmod()
