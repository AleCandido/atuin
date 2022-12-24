from functools import reduce

from . import tphon


def show():
    return list(filter(lambda m: not m.startswith("_"), dir(tphon)))


def sum(*args):
    if len(args) == 1:
        return sum(*args[0])

    return reduce(lambda x, y: tphon.sum_as_string(int(x), y), args, "0")
