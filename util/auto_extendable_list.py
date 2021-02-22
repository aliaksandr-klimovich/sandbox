class auto_extendable_list(list):
    """
    This class implements auto expandable list.

    The idea was to implement lists like in JavaScript, i.e.
        if you set a value in the list at non existing index,
        then the value is set anyway, expanding the list with empty data.

    The auto_extendable_list is expanded with None values by default.
    """

    FILL_VALUE = None

    def __setitem__(self, index: int, value):
        if len(self) <= index:
            addon = index - len(self) + 1
            self.extend([self.FILL_VALUE] * addon)
        super().__setitem__(index, value)


if __name__ == '__main__':
    import unittest

    class TestCase(unittest.TestCase):
        def setUp(self) -> None:
            self.a = auto_extendable_list()

        def test_add_value_at_index_0(self):
            "Test that list is auto expanding and the value is set."
            self.a[0] = 0
            self.assertEqual(self.a, [0])

        def test_add_value_at_index_1(self):
            "Test that list is expanding to correct length and has correct fill value."
            self.a[1] = 1
            self.assertEqual(self.a, [None, 1])

        def test_modify_value_at_existing_index(self):
            "That that list is not expanding and the value at index is changing."
            self.a.extend([0, 1, 2])
            self.a[1] = 3
            self.assertEqual(self.a, [0, 3, 2])

    suite = unittest.makeSuite(TestCase)
    runner = unittest.TextTestRunner()
    runner.run(suite)
