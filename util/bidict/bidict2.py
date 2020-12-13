class bidict(dict):
    """
    Implementation of bidirectional dictionary.
    This kind of dictionary stores {key: key} pair.
    The main idea is to access each key using sibling key.

    Current implementation stores 1 pair of key-value in self dictionary,
    like a regular dict, but it is possible to obtain key by value.
    """

    def __getitem__(self, key):
        for k, v in self.items():
            if k == key:
                return v
            elif v == key:
                return k
        raise KeyError(key)

    def __setitem__(self, key, value):
        # this introduces a huge processing time when adding new variables
        for k, v in self.items():
            if v == key:
                del self[k]
                break
        super().__setitem__(key, value)


if __name__ == '__main__':
    import unittest

    class TestBiDict(unittest.TestCase):
        def test_getitem(self):
            bd = bidict({'a': 1})
            self.assertEqual(bd['a'], 1)
            self.assertEqual(bd[1], 'a')
            with self.assertRaises(KeyError):
                bd[0]

        def test_non_trivial_behavior(self):
            # if comment __setitem__ function, this code will behave differently
            bd = bidict()
            bd['a'] = 1
            bd[1] = 'b'  # at this point pair {'a': 1}  is removed
            self.assertEqual(bd[1], 'b')
            with self.assertRaises(KeyError):
                bd['a']

    unittest.main()
