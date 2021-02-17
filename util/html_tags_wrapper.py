import sys

OUTPUT = sys.stdout


class html_meta(type):

    def __getattr__(cls, tag_name):

        def _init(self, **attrs):
            self._attrs = attrs

        def _print_opening_tag(self):
            print(f'<{tag_name}', end='', file=OUTPUT)
            for k, v in self._attrs.items():
                print(f' {k}="{v}"', end='', file=OUTPUT)
            print('>', end='', file=OUTPUT)

        def _print_closing_tag(self):
            print(f'</{tag_name}>', end='', file=OUTPUT)

        def _enter(self):
            self._print_opening_tag()

        def _exit(self, exc_type, exc_val, exc_tb):
            self._print_closing_tag()

        def _call(self, text):
            self._print_opening_tag()
            print(text, end='', file=OUTPUT)
            self._print_closing_tag()

        tag_class = type(tag_name, (), {
            '__slots__': ('_attrs', ),
            '_print_opening_tag': _print_opening_tag,
            '_print_closing_tag': _print_closing_tag,
            '__init__': _init,
            '__enter__': _enter,
            '__exit__': _exit,
            '__call__': _call,
        })

        return tag_class


class html(metaclass=html_meta):
    pass


if __name__ == '__main__':
    import unittest
    from io import StringIO

    class TestCase(unittest.TestCase):
        @classmethod
        def tearDownClass(cls):
            global OUTPUT
            OUTPUT = sys.stdout

        def setUp(self):
            global OUTPUT
            OUTPUT = StringIO()

        def tearDown(self):
            OUTPUT.close()

        def test_html_context_manager(self):
            assert isinstance(OUTPUT, StringIO)  # for IDE method provision
            with html.u(style='color:red'):
                print('test', end='', file=OUTPUT)
            text = OUTPUT.getvalue()
            self.assertEqual(text, '<u style="color:red">test</u>')

        def test_html_call(self):
            assert isinstance(OUTPUT, StringIO)  # for IDE method provision
            html.u(style='color:red')('test')
            text = OUTPUT.getvalue()
            self.assertEqual(text, '<u style="color:red">test</u>')

    suite = unittest.makeSuite(TestCase)
    runner = unittest.TextTestRunner()
    runner.run(suite)
