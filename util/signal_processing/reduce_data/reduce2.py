from typing import Any
from collections.abc import Iterator, Generator
from operator import itemgetter
from itertools import groupby


# It's slow..., but easy to implement.
def reduce2(data: Iterator) -> Generator[Any]:
    """
    Returns reduced list of values. Sibling values are grouped by value.

    Example:
    >>> list(reduce2([1, 2, 2, 3, 3, 3, 1]))
    [1, 2, 3, 1]

    """
    yield from map(itemgetter(0), groupby(data))
