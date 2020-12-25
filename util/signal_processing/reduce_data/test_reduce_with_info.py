import unittest
from reduce_with_info import reduce_with_info


class TestCase(unittest.TestCase):
    def test(self):
        test_data = (
            ([], []),
            ([0], [(0, 0, 1)]),
            ([0, 1], [(0, 0, 1), (1, 1, 1)]),
            ([0, 0], [(0, 0, 2)]),
            ([0, 0, 1], [(0, 0, 2), (2, 1, 1)]),
            ([1, 0, 0], [(0, 1, 1), (1, 0, 2)]),
            ([0, 0, 1, 0], [(0, 0, 2), (2, 1, 1), (3, 0, 1)]),
            ([0, 1, 0, 0], [(0, 0, 1), (1, 1, 1), (2, 0, 2)]),
            ([0, 1, 1, 0], [(0, 0, 1), (1, 1, 2), (3, 0, 1)]),
            ([0, 0, 1, 1, 0, 0], [(0, 0, 2), (2, 1, 2), (4, 0, 2)]),
            ([None, None], [(0, None, 2)]),
        )
        for input_, exp_output in test_data:
            with self.subTest(input_=input_, exp_output=exp_output):
                data = list(reduce_with_info(input_))

                self.assertEqual(data, exp_output)


if __name__ == '__main__':
    unittest.main()
