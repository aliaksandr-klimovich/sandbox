from typing import Union


def get_reduced_list2(data: Union[list, tuple]) -> list:
    result = []
    if not data:
        return result
    prev = data[0]
    result.append(prev)
    for curr in data[1:]:
        if prev != curr:
            prev = curr
            result.append(curr)
    return result
