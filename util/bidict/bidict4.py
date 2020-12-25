import weakref


class bidict:
    """

       keys 1                 keys 2
    {  1 : lnk_to_2 }      {  2 : lnk_to_1 }
    {  2 : lnk_to_1 }

    >>> bd = bidict()
    >>> bd['x'] = 1
    >>> bd.keys1

    todo ...
    """

    def __init__(self):
        self.keys1 = dict()
        self.keys2 = dict()

    def __setitem__(self, key1, key2):
        self.keys1[key1] = None
        self.keys2[key2] = None
        self.keys1[key1] = weakref()
        ...

    def __getitem__(self, key):
        try:
            value = self.keys1[key]
        except KeyError:
            try:
                value = self.keys2[key]
            except KeyError:
                raise KeyError(key)
        return value
