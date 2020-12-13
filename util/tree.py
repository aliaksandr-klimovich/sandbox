from collections import defaultdict


class PrettyDefaultDict(defaultdict):
    def __str__(self):
        return dict.__str__(self)

    def __repr__(self):
        return dict.__repr__(self)


def tree():
    """
    >>> t = tree()
    >>> t['a']['b']['c'] = 1
    >>> t
    {'a': {'b': {'c': 1}}}
    """
    return PrettyDefaultDict(tree)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
