from functools import reduce

from atuin import _atuin


def show():
    return list(filter(lambda m: not m.startswith("_"), dir(_atuin)))


def sum(*args):
    if len(args) == 1:
        return sum(*args[0])

    return reduce(lambda x, y: _atuin.sum_as_string(int(x), y), args, "0")
