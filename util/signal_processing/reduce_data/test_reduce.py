import unittest
from reduce import reduce


class TestReduce(unittest.TestCase):
    def test(self):
        test_data = (
            ([], []),
            ([1], [1]),
            ([1, 2], [1, 2]),
            ([1, 1], [1]),
            ([1, 1, 2], [1, 2]),
            ([1, 2, 2], [1, 2]),
            ([1, 2, 1], [1, 2, 1]),
            ([None, None, 1], [None, 1]),
        )
        for input_, exp_output in test_data:
            with self.subTest(input_=input_, exp_output=exp_output):
                sections = list(reduce(input_))
                self.assertEqual(sections, exp_output)


if __name__ == '__main__':
    unittest.main()
