from collections.abc import Iterator, Generator
from typing import Any


def reduce(data: Iterator) -> Generator[Any]:
    """
    Returns reduced list of values. Sibling values are grouped by value.

    Example:
    >>> list(reduce([1, 2, 2, 3, 3, 3, 1]))
    [1, 2, 3, 1]
    """
    iter_data = iter(data)
    try:
        previous_value = next(iter_data)
    except StopIteration:
        return
    yield previous_value
    for current_value in iter_data:
        if current_value != previous_value:
            yield current_value
            previous_value = current_value
