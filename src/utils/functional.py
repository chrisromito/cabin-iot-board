from typing import Callable, Dict, List

from constants import MILLION, ONE, ZERO


def clamp(lower, upper, value):
    return max(lower, min(value, upper))


def c_clamp(lower, upper):
    def _c_clamp(value):
        return clamp(lower, upper, value)

    return _c_clamp


def microsec_to_duty(freq, width_microsec):
    """
    WiPy needs duty cycles as a decimal percent, but that can be a PITA to calculate on the fly.

    If we have these variables:
    T = time (seconds)
    F = frequency (Hz)
    P = pulse width
    D = duty cycle as decimal % (what WiPy needs)

    We can calculate the duty cycle % using these equations:
    T = 1 / F
    D = P / T
    """
    t = ONE / freq
    p = width_microsec / MILLION
    d = p / t
    return clamp(ZERO, ONE, d)


# Functional utils
# #######################
def map_right(fn: Callable):
    return lambda l: list(map(fn, l))


def merge(dict_list: List[Dict]):
    temp = {}
    for d in dict_list:
        temp.update(d)
    return temp


# Object Attributes
def prop(name: str):
    def _prop(obj):
        return getattr(obj, name, None)

    return _prop


def props(*args: str):
    def _props(obj):
        return [
            getattr(obj, arg, None)
            for arg in args
        ]

    return _props


# Dict Operators
def key(k):
    def _key(d):
        try:
            return d[k]
        except KeyError:
            return None

    return _key


def _key_right(d):
    return lambda k: key(k)(d)


def keys(*args):
    def _keys(d):
        partial_keys = _key_right(d)
        return [partial_keys(arg) for arg in args]

    return _keys


# Tuple/List operators
def index(n):
    def _index(o):
        try:
            return o[n]
        except IndexError:
            return None

    return _index


def _index_right(obj):
    return lambda _index: index(_index)(obj)


def indexes(*args):
    def _indexes(obj):
        partial_indexes = _index_right(obj)
        return [
            partial_indexes(arg) for arg in args
        ]

    return _indexes
