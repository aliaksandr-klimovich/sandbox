class bidict(dict):
    """
    Implementation of bidirectional dictionary.
    This kind of dictionary stores {key: key} pair.
    The main idea is to access each key using sibling key.

    Current implementation stores 2 pairs of key-values in self dictionary
    as {key: value} and {value: key}.

    Restriction:
        Each key should be hashable type.
    """
    def __init__(self, *args, **kwargs):
        # create first {key: value} pair
        super().__init__(*args, **kwargs)
        # create second pair {value: key}
        for key, value in kwargs.items():  # process kwargs (e.g. a=1, b=2)
            self[value] = key
        if args:  # process args (e.g. {'a': 1})
            for key, value in args[0].items():  # todo add non dict type support
                self[value] = key

    def __setitem__(self, key, value):
        # reset two pairs
        if key in self:
            del self[key]
        # the {value: key} pair will be deleted in __delitem__
        super().__setitem__(key, value)
        super().__setitem__(value, key)

    def __delitem__(self, key):
        # remove two pairs
        value = self[key]
        super().__delitem__(key)
        try:
            super().__delitem__(value)
        except KeyError:
            pass


if __name__ == '__main__':
    import unittest

    class TestBiDict(unittest.TestCase):

        def test_init(self):
            bd = bidict()
            self.assertEqual(bd, {})
            bd = bidict({'a': 1})
            self.assertEqual(bd, {'a': 1, 1: 'a'})
            bd = bidict(a=1)
            self.assertEqual(bd, {'a': 1, 1: 'a'})
            bd = bidict({'a': 1}, b=2)
            self.assertEqual(bd, {'a': 1, 1: 'a', 'b': 2, 2: 'b'})

        def test_setitem(self):
            bd = bidict()
            bd['a'] = 1
            self.assertEqual(bd, {'a': 1, 1: 'a'})
            bd['a'] = 2
            self.assertEqual(bd, {'a': 2, 2: 'a'})
            bd[2] = 'b'
            self.assertEqual(bd, {'b': 2, 2: 'b'})
            bd[3] = 3  # key == value

        def test_delitem(self):
            bd = bidict({'a': 1})
            del bd['a']
            self.assertEqual(bd, {})
            bd = bidict({'a': 1})
            del bd[1]
            self.assertEqual(bd, {})
            bd = bidict({0: 0})
            del bd[0]
            self.assertEqual(bd, {})

    unittest.main()
