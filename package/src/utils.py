
import collections


def flatten_nested_list(nested_list):
    """Flattern a list by returning all the elements as a generator"""

    for el in nested_list:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten_nested_list(el)
        else:
            yield el