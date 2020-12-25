import unittest
from reduce_with_tolerance import reduce_with_tolerance


class TestCase(unittest.TestCase):
    def test(self):
        test_data = (
            # with tolerance set to zero, repeat tests that are implemented for `reduce` function
            ([], 0, []),
            ([1], 0, [(1,)]),
            ([1, 2], 0, [(1,), (2,)]),
            ([1, 1], 0, [(1, 1)]),
            ([1, 1, 2], 0, [(1, 1), (2,)]),
            ([1, 2, 2], 0, [(1,), (2, 2)]),
            ([1, 2, 1], 0, [(1,), (2,), (1,)]),
            # with tolerance
            ([], 1, []),
            ([1], 1, [(1,)]),
            ([1, 2], 1, [(1, 2)]),
            ([1, 1], 1, [(1, 1)]),
            ([1, 1, 2], 1, [(1, 1, 2)]),
            ([1, 2, 2], 1, [(1, 2, 2)]),
            ([1, 2, 1], 1, [(1, 2, 1)]),
            # with different border distance
            ([1, 2, 3], 1, [(1, 2), (3,)]),
            ([1, 3, 2], 1, [(1,), (3, 2)]),
            # reversed
            ([3, 2, 1], 1, [(3, 2), (1,)]),
            ([3, 1, 2], 1, [(3,), (1, 2)]),
        )
        for data, tolerance, exp_output in test_data:
            with self.subTest(data=data, tolerance=tolerance, exp_output=exp_output):
                output = list(reduce_with_tolerance(data, tolerance))
                self.assertEqual(output, exp_output)


if __name__ == '__main__':
    unittest.main()
