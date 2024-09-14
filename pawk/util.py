""" Some util functions """

def detect_last(iterable):
    """
    Yield items as pairs with a bool, the bool is true for the last element in
    the iterable.

    >>> list(detect_last([1, 2, 3]))
    [(1, False), (2, False), (3, True)]
    >>> list(detect_last([1]))
    [(1, True)]
    >>> list(range(0))
    []
    """
    _iter = iter(iterable)
    try:
        a = next(_iter)
    except StopIteration:
        return
    for b in _iter:
        yield a, False
        a = b
    yield a, True


def intify(word):
    """Try to parse as numbers if possible"""
    try:
        return int(word)
    except ValueError:
        return word
