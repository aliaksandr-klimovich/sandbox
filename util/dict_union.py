import builtins
from typing import Dict


def dict_union(*args: Dict) -> Dict:
    """
    Unite two or more dicts into one.
    Results in a new dict.

    >>> dict_union({'a': 1}, {'b': 2})
    {'a': 1, 'b': 2}
    """
    new_dict = {}
    for dict_ in args:
        new_dict.update(dict_)
    return new_dict


# redefine a built-in dict
class dict(builtins.dict):
    """
    Dict that has `dict_union` implementation.
    It is used for unite two or more dicts into one.
    Return value is a new dict.

    >>> dict(a=1) + dict(b=2) + dict(c=3)
    {'a': 1, 'b': 2, 'c': 3}
    """

    def __add__(self, *args):
        return dict.union(self, *args)

    @staticmethod
    def union(*args):
        new_dict = dict()
        for d in args:
            new_dict.update(d)
        return new_dict
