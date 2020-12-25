from typing import Union


def get_reduced_list3(data: Union[list, tuple]) -> list:
    result = []
    if not data:
        return result
    prev = data[0]
    result.append(prev)
    for i in range(1, len(data)):
        curr = data[i]
        if prev != curr:
            prev = curr
            result.append(curr)
    return result
