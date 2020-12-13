import sys


if sys.version_info.major == 2:
    # the `flatten` function can be found in compiler library:
    # `from compiler.ast import flatten`

    from collections import Iterable

    def flatten(iterable):
        for i in iterable:
            # if type(t) is list or type(t) is tuple:  # strict check
            # if isinstance(i, list) or isinstance(i, tuple):  # with instances of lists or tuples
            if isinstance(i, Iterable) and not isinstance(i, str):  # non strict check
                for j in flatten(i):
                    yield j
            else:
                yield i

elif sys.version_info.major == 3:
    from collections.abc import Iterable

    def flatten(iterable):

        for i in iterable:

            try:
                iter(i)
            except TypeError:
                is_iterable = False
            else:
                is_iterable = True

            if is_iterable and not isinstance(i, str):
                yield from flatten(i)
            else:
                yield i


if __name__ == '__main__':
    import unittest

    class TC(unittest.TestCase):
        def test_flatten(self):
            iterable = [1, '2', [3, 4], [5, [('6', ), (('76', ), )]]]
            expected_result = [1, '2', 3, 4, 5, '6', '76']
            result = list(flatten(iterable))
            self.assertEqual(result, expected_result)

    unittest.main()
