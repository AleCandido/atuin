from functools import reduce

from atuin import _atuin


def show():
    print(dir(_atuin))


def sum(*args):
    return reduce(lambda x, y: _atuin.sum_as_string(int(x), y), args, "0")
