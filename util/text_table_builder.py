from functools import wraps
from typing import Union, Iterator, Tuple, List, Type


# def cached(f):
#     ret_val = []
#     @wraps(f)
#     def wrapper(self):
#         if not ret_val:
#             ret_val.append(f(self))
#         return ret_val[0]
#     return wrapper


class TextTableBuilderException(Exception):
    pass


class TextTableBuilderWarning(Warning):
    pass


class TextTableStyle:
    """
    Prototype for table style.
    """
    horizontal = ''
    vertical = ''
    down_and_right = ''
    down_and_left = ''
    up_and_right = ''
    up_and_left = ''
    vertical_and_right = ''
    vertical_and_left = ''
    down_and_horizontal = ''
    up_and_horizontal = ''
    vertical_and_horizontal = ''


class LightTextTableStyle(TextTableStyle):
    horizontal = '─'
    vertical = '│'
    down_and_right = '┌'
    down_and_left = '┐'
    up_and_right = '└'
    up_and_left = '┘'
    vertical_and_right = '├'
    vertical_and_left = '┤'
    down_and_horizontal = '┬'
    up_and_horizontal = '┴'
    vertical_and_horizontal = '┼'


class SimpleTextTableStyle(TextTableStyle):
    horizontal = '-'
    vertical = '|'
    down_and_right = '*'
    down_and_left = '*'
    up_and_right = '*'
    up_and_left = '*'
    vertical_and_right = '*'
    vertical_and_left = '*'
    down_and_horizontal = '*'
    up_and_horizontal = '*'
    vertical_and_horizontal = '*'


class ArcCornersTextTableStyle(LightTextTableStyle):
    down_and_right = '╭'
    down_and_left = '╮'
    up_and_right = '╰'
    up_and_left = '╯'


class DoubleTextTableStyle(TextTableStyle):
    horizontal = '═'
    vertical = '║'
    down_and_right = '╔'
    down_and_left = '╗'
    up_and_right = '╚'
    up_and_left = '╝'
    vertical_and_right = '╠'
    vertical_and_left = '╣'
    down_and_horizontal = '╦'
    up_and_horizontal = '╩'
    vertical_and_horizontal = '╬'


TextTableStyle.Light = LightTextTableStyle
TextTableStyle.Simple = SimpleTextTableStyle
TextTableStyle.Arc = ArcCornersTextTableStyle
TextTableStyle.Double = DoubleTextTableStyle


class MixedTextTableStyle(TextTableStyle):
    """
    Prototype for mixed heavy and light styles.
    Headers are heavy printed, rows are light printed.
    """
    heavy_horizontal = ''
    heavy_vertical = ''
    heavy_down_and_right = ''
    heavy_down_and_left = ''
    heavy_up_and_right = ''
    heavy_up_and_left = ''
    down_light_and_right_up_heavy = ''
    up_light_and_right_down_heavy = ''
    down_light_and_left_up_heavy = ''
    up_light_and_left_down_heavy = ''
    heavy_down_and_horizontal = ''
    heavy_up_and_horizontal = ''
    down_light_and_up_horizontal_heavy = ''
    up_light_and_down_horizontal_heavy = ''


class HeavyAndLightTextTableStyle(MixedTextTableStyle, LightTextTableStyle):
    heavy_horizontal = '━'
    heavy_vertical = '┃'
    heavy_down_and_right = '┏'
    heavy_down_and_left = '┓'
    heavy_up_and_right = '┗'
    heavy_up_and_left = '┛'
    down_light_and_right_up_heavy = '┡'
    up_light_and_right_down_heavy = '┢'
    down_light_and_left_up_heavy = '┩'
    up_light_and_left_down_heavy = '┪'
    heavy_down_and_horizontal = '┳'
    heavy_up_and_horizontal = '┻'
    down_light_and_up_horizontal_heavy = '╇'
    up_light_and_down_horizontal_heavy = '╈'


TextTableStyle.HeavyAndLight = HeavyAndLightTextTableStyle


class TextTableBuilder:
    """
    Builds a table in text representation.
    """

    # todo introduce widths:
    #  list of widths for each column

    # todo introduce word wrap functionality

    def __init__(self,
                 header: Union[Tuple, List],
                 data: Union[Tuple[Iterator], List[Iterator]],
                 style: Type[TextTableStyle] = SimpleTextTableStyle,
                 min_cell_width: int = 0,
                 insert_header_every_n_rows: int = 20,
                 insert_header_at_the_bottom: bool = False,
                 build_and_print_immediately: bool = True):
        """
        :param header:
            Table header. List of names.
        :param data:
            List of variables.
            Each element should contain a list of values.
            Example:
                f(x) = 2*x
                header = ('x', 'f(x)')
                data = ((1, 2, 3), (2, 4, 6))
        :param build_and_print_immediately:
            To build the table immediately (starting from the class constructor) or not.
            If this parameter is False, you'll need to call `build` method later on and then `print`
              (or just `print`).
        :param style:
            TextTableStyle to use to print table. Prototype is given in TextTableStyle class.
            Also you can apply mixed style. Prototype is given in MixedStyle class.
        """

        # Initialize variables.
        self.header = header
        self.data = data
        self.style = style
        self.min_cell_width = min_cell_width
        self.insert_header_every_n_rows = insert_header_every_n_rows
        self.insert_header_at_the_bottom = insert_header_at_the_bottom
        # build_and_print_immediately is not stored in class instance

        # Define private variables.
        self._widths: List[int]
        self._top_row: str
        self._bottom_row: str
        self._delimiter: str
        self._head: str
        self._rows: str

        # Private variables for mixed style.
        self._delimiter_up_light_down_heavy: str
        self._delimiter_up_heavy_down_light: str
        self._bottom_row_heavy: str

        # A switch to indicate if table was built.
        self._built = False

        if build_and_print_immediately:
            self.print()

    def _find_widths(self):
        """
        Finds maximum width for each column depending on all variables.
        Uses ``self.header`` and ``self.data`` to calculate maximum column widths.
        Note, this is a first most consuming build step.
        """
        widths = []
        for name, variable in zip(self.header, self.data):
            width = self.min_cell_width
            len_name = len(str(name))
            if len_name > self.min_cell_width:
                width = len_name
            for value in variable:
                len_value = len(str(value))
                if len_value > width:
                    width = len_value
            widths.append(width)
        self._widths = widths

    def _build_delimiter(self):
        """
        Builds a delimiter between header row in a table.
        """
        delimiter = [self.style.vertical_and_right]
        middle = []
        for width in self._widths:
            middle.append(self.style.horizontal * (width + 2))
        delimiter.append(self.style.vertical_and_horizontal.join(middle))
        delimiter.append(self.style.vertical_and_left)
        self._delimiter = ''.join(delimiter)

    def _build_delimiter_up_light_down_heavy(self):
        """
        Builds a delimiter to connect top data with bottom header.
        Valid only with mixed style.
        """
        assert issubclass(self.style, MixedTextTableStyle)
        delimiter = [self.style.up_light_and_right_down_heavy]
        middle = []
        for width in self._widths:
            middle.append(self.style.heavy_horizontal * (width + 2))
        delimiter.append(self.style.up_light_and_down_horizontal_heavy.join(middle))
        delimiter.append(self.style.up_light_and_left_down_heavy)
        self._delimiter_up_light_down_heavy = ''.join(delimiter)

    def _build_delimiter_up_heavy_down_light(self):
        """
        Builds a delimiter to connect top header with bottom data.
        Valid only with mixed style.
        """
        assert issubclass(self.style, MixedTextTableStyle)
        delimiter = [self.style.down_light_and_right_up_heavy]
        middle = []
        for width in self._widths:
            middle.append(self.style.heavy_horizontal * (width + 2))
        delimiter.append(self.style.down_light_and_up_horizontal_heavy.join(middle))
        delimiter.append(self.style.down_light_and_left_up_heavy)
        self._delimiter_up_heavy_down_light = ''.join(delimiter)

    def _build_top_row(self):
        """
        Builds top row of a table.
        """
        if issubclass(self.style, MixedTextTableStyle):
            horizontal = self.style.heavy_horizontal
            down_and_right = self.style.heavy_down_and_right
            down_and_horizontal = self.style.heavy_down_and_horizontal
            down_and_left = self.style.heavy_down_and_left
        else:
            horizontal = self.style.horizontal
            down_and_right = self.style.down_and_right
            down_and_horizontal = self.style.down_and_horizontal
            down_and_left = self.style.down_and_left

        top_row = [down_and_right]
        middle = []
        for width in self._widths:
            middle.append(horizontal * (width + 2))
        top_row.append(down_and_horizontal.join(middle))
        top_row.append(down_and_left)
        self._top_row = ''.join(top_row)

    def _build_bottom_row(self):
        """
        Builds bottom row of a table.
        """
        bottom_row = [self.style.up_and_right]
        middle = []
        for width in self._widths:
            middle.append(self.style.horizontal * (width + 2))
        bottom_row.append(self.style.up_and_horizontal.join(middle))
        bottom_row.append(self.style.up_and_left)
        self._bottom_row = ''.join(bottom_row)

    def _build_bottom_row_heavy(self):
        """
        Builds bottom row of a table.
        Valid only with mixed style.
        """
        assert issubclass(self.style, MixedTextTableStyle)
        bottom_row = [self.style.heavy_up_and_right]
        middle = []
        for width in self._widths:
            middle.append(self.style.heavy_horizontal * (width + 2))
        bottom_row.append(self.style.heavy_up_and_horizontal.join(middle))
        bottom_row.append(self.style.heavy_up_and_left)
        self._bottom_row_heavy = ''.join(bottom_row)

    def _build_head(self):
        """
        Builds a header of a table from ``self._names`` using ``self._widths``.
        """
        vertical = self.style.heavy_vertical if issubclass(self.style, MixedTextTableStyle) else self.style.vertical

        head = [vertical]
        for name, width in zip(self.header, self._widths):
            head.append(f' {name:<{width}} ' + vertical)
        self._head = ''.join(head)

    def _build_rows(self):
        """
        Builds rows of a table from ``self.data``.
        Note, this is a second most consuming build steps.
        """
        rows = []
        for variables in zip(*self.data):
            row = [self.style.vertical]
            for width, variable in zip(self._widths, variables):
                row.append(f' {variable:<{width}} ' + self.style.vertical)
            row = ''.join(row)
            rows.append(row)
        self._rows = rows

    def _iter_build_rows(self):
        for variables in zip(*self.data):
            row = [self.style.vertical]
            for width, variable in zip(self._widths, variables):
                row.append(f' {variable:<{width}} {self.style.vertical}')
            row = ''.join(row)
            yield row

    def _build_table_structure(self):
        """
        Build a table structure.
        """
        self._find_widths()
        self._build_top_row()
        self._build_bottom_row()

        if issubclass(self.style, MixedTextTableStyle):
            self._build_delimiter_up_light_down_heavy()
            self._build_delimiter_up_heavy_down_light()
        else:
            self._build_delimiter()

        self._build_head()
        self._build_rows()

    def _print_table(self):
        """
        Actually prints a table.
        """
        print(self._top_row)
        print(self._head)
        if issubclass(self.style, MixedTextTableStyle):
            print(self._delimiter_up_heavy_down_light)
        else:
            print(self._delimiter)

        if self.insert_header_every_n_rows:
            for i, row in enumerate(self._rows):
                # Check whether need to inset the header.
                if i != 0 and i % self.insert_header_every_n_rows == 0:
                    if issubclass(self.style, MixedTextTableStyle):
                        print(self._delimiter_up_light_down_heavy)
                    else:
                        print(self._delimiter)
                    print(self._head)
                    if issubclass(self.style, MixedTextTableStyle):
                        print(self._delimiter_up_heavy_down_light)
                    else:
                        print(self._delimiter)
                print(row)
        else:
            for row in self._rows:
                print(row)

        if self.insert_header_at_the_bottom:
            if issubclass(self.style, MixedTextTableStyle):
                print(self._delimiter_up_light_down_heavy)
            else:
                print(self._delimiter)
            print(self._head)
            if issubclass(self.style, MixedTextTableStyle):
                print(self._bottom_row_heavy)
            else:
                print(self._bottom_row)
        else:
            print(self._bottom_row)

    def build(self):
        self._build_table_structure()
        self._built = True
        return self

    def print(self):
        if not self._built:
            self.build()
        self._print_table()

    def iter_print(self):
        for line in self._iter_get_line():
            print(line)

    def _iter_get_line(self):
        self._find_widths()

        self._build_top_row()
        yield self._top_row

        self._build_head()
        yield self._head

        if issubclass(self.style, MixedTextTableStyle):
            self._build_delimiter_up_light_down_heavy()
            self._build_delimiter_up_heavy_down_light()
            yield self._delimiter_up_heavy_down_light
        else:
            self._build_delimiter()
            yield self._delimiter

        if self.insert_header_every_n_rows:
            i = 0
            for row in self._iter_build_rows():
                if i == self.insert_header_every_n_rows:
                    if issubclass(self.style, MixedTextTableStyle):
                        yield self._delimiter_up_light_down_heavy
                    else:
                        yield self._delimiter
                    yield self._head
                    if issubclass(self.style, MixedTextTableStyle):
                        yield self._delimiter_up_heavy_down_light
                    else:
                        yield self._delimiter
                    i = 0
                else:
                    i += 1
                yield row
        else:
            yield from self._iter_build_rows()

        if self.insert_header_at_the_bottom:
            if issubclass(self.style, MixedTextTableStyle):
                yield self._delimiter_up_light_down_heavy
            else:
                yield self._delimiter
            yield self._head
            if issubclass(self.style, MixedTextTableStyle):
                self._build_bottom_row_heavy()
                yield self._bottom_row_heavy
            else:
                self._build_bottom_row()
                yield self._bottom_row
        else:
            self._build_bottom_row()
            yield self._bottom_row


if __name__ == '__main__':
    # smoke test
    n = 6
    a = (1,) * n
    b = (-12345678901234567890.12345678901234567890,) * (n+1)
    tb = TextTableBuilder(['a', 'second variable name .............'], [a, b], TextTableStyle.Arc,
                          min_cell_width=10,
                          insert_header_at_the_bottom=True,
                          insert_header_every_n_rows=3,
                          build_and_print_immediately=False)
    tb.iter_print()
