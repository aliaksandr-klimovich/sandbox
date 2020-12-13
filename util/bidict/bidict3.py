class BiDict:
    def __init__(self, *args, **kwargs):
        self._storage = []
        for container in args:
            if isinstance(container, dict):
                for k, v in container.items():
                    self._check_for_duplicate(k, v)
                    self._storage.append((k, v))
            elif isinstance(container, tuple) or isinstance(container, list):
                for pair in container:
                    if isinstance(pair, dict):
                        for k, v in pair.items():
                            self._check_for_duplicate(k, v)
                            self._storage.append((k, v))
                        continue
                    if not (isinstance(pair, tuple) or isinstance(pair, list)) or len(pair) != 2:
                        raise ValueError(pair)
                    k = pair[0]
                    v = pair[1]
                    self._check_for_duplicate(k, v)
                    self._storage.append((k, v))
            else:
                raise ValueError(container)
        for k, v in kwargs.items():
            self._check_for_duplicate(k, v)
            self._storage.append((k, v))

    def __getitem__(self, key):
        for item1, item2 in self._storage:
            if item1 == key:
                return item2
            if item2 == key:
                return item1
        raise KeyError(key)

    def __setitem__(self, key, value):
        try:
            self.__delitem__(key)
        except KeyError:
            pass

        try:
            self.__delitem__(value)
        except KeyError:
            pass

        self._storage.append((key, value))

    def __delitem__(self, key):
        for i, (item1, item2) in enumerate(self._storage):
            if item1 == key or item2 == key:
                self._storage.pop(i)
                break
        else:
            raise KeyError(key)

    def _check_for_duplicate(self, key, value):
        for item1, item2 in self._storage:
            if item1 == key or item1 == value or \
               item2 == key or item2 == value:
                raise DuplicateError('{{{}: {}}} duplicates {{{}: {}}}'.format(key, value, item1, item2))

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()


class DuplicateError(LookupError):
    pass


if __name__ == '__main__':
    import unittest

    class TestInit(unittest.TestCase):
        def test_no_param(self):
            d = BiDict()
            self.assertEqual(d._storage, [])

        def test_dict(self):
            d = BiDict({'a': 1})
            self.assertEqual(d._storage, [('a', 1)])

        def test_kwarg(self):
            d = BiDict(a=1)
            self.assertEqual(d._storage, [('a', 1)])

        def test_dict_kwarg(self):
            d = BiDict({'a': 1}, b=2)
            self.assertEqual(d._storage, [('a', 1), ('b', 2)])

        def test_list_tuple(self):
            d = BiDict([('a', 1), ('b', 2)])
            self.assertEqual(d._storage, [('a', 1), ('b', 2)])

        def test_tuple_tuple(self):
            d = BiDict((('a', 1), ('b', 2)))
            self.assertEqual(d._storage, [('a', 1), ('b', 2)])

        def test_tuple_list(self):
            d = BiDict((['a', 1], ['b', 2]))
            self.assertEqual(d._storage, [('a', 1), ('b', 2)])

        def test_list_list(self):
            d = BiDict([['a', 1], ['b', 2]])
            self.assertEqual(d._storage, [('a', 1), ('b', 2)])

        def test_dict_tuple(self):
            d = BiDict([{'a': 1}, ('b', 2)])
            self.assertEqual(d._storage, [('a', 1), ('b', 2)])

        def test_dict_tuple_list_kwarg(self):
            d = BiDict({'a': 1}, (('b', 2), ), [['c', 3]], d=4)
            self.assertEqual(d._storage, [('a', 1), ('b', 2), ('c', 3), ('d', 4)])

        def test_bad_arg(self):
            with self.assertRaises(ValueError):
                BiDict('ab')

        def test_bad_list_item(self):
            with self.assertRaises(ValueError):
                BiDict(['ab'])

        def test_duplicate_dict(self):
            with self.assertRaises(DuplicateError):
                BiDict({'a': 1, 'b': 1})

        def test_duplicate_kwargs(self):
            with self.assertRaises(DuplicateError):
                BiDict(a=1, b=1)

        def test_duplicate_dict_kwarg(self):
            with self.assertRaises(DuplicateError):
                BiDict({'a': 1}, b=1)

    class TestSetItem(unittest.TestCase):
        def test_one_item(self):
            d = BiDict()
            d['a'] = 1
            self.assertEqual(d._storage, [('a', 1)])

        def test_two_items(self):
            """Test sequence in which the items are added/stored"""
            d = BiDict()
            d['b'] = 1
            d['a'] = 2
            self.assertEqual(d._storage, [('b', 1), ('a', 2)])

        def test_rewrite_by_key(self):
            d = BiDict(a=1)
            d[1] = 'c'
            self.assertEqual(d._storage, [(1, 'c')])

        def test_rewrite_by_value(self):
            d = BiDict(a=1)
            d['a'] = 2
            self.assertEqual(d._storage, [('a', 2)])

        def test_rewrite_by_key_and_value(self):
            d = BiDict(a=1, b=2)
            d[2] = 1
            self.assertEqual(d._storage, [(2, 1)])

    class TestGetItem(unittest.TestCase):
        def test_by_key(self):
            d = BiDict(a=1)
            self.assertEqual(d['a'], 1)

        def test_by_value(self):
            d = BiDict(a=1)
            self.assertEqual(d[1], 'a')

        def test_not_existing(self):
            d = BiDict()
            with self.assertRaises(KeyError):
                d[0]

    class TestDelItem(unittest.TestCase):
        def test_by_key(self):
            d = BiDict(a=1)
            del d['a']
            self.assertEqual(d._storage, [])

        def test_by_value(self):
            d = BiDict(a=1)
            del d[1]
            self.assertEqual(d._storage, [])

        def test_not_existing(self):
            d = BiDict()
            with self.assertRaises(KeyError):
                del d[0]

    unittest.main()
