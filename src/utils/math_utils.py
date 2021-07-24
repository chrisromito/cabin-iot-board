"""
Math utils & types
"""
from typing import Union, List, Tuple

from constants import TWO


def scale(from_min, from_max, to_min, to_max):
    from_diff = from_max - from_min
    to_diff = to_max - to_min

    def _scale(n):
        left = (n - from_min) * to_diff
        return (left / from_diff) + to_min

    return _scale


Number = Union[float, int]


def mean(data: Union[Number, List[Number], Tuple[Number]]) -> float:
    if iter(data) is data:
        data = list(data)
    return sum(data) / len(data)


def square(n: Number) -> float:
    return math.pow(n, TWO)


def square_root(n: Number) -> float:
    return math.sqrt(n)


def hypot(a: Number, b: Number) -> float:
    return square_root(
        square(a) + square(b)
    )


def hypotenuse(a, b) -> float:
    return hypot(a, b)


def divide(a, b) -> float:
    try:
        return a / b
    except ZeroDivisionError:
        return a / 0.00001


def product(*args: float) -> float:
    value = 1
    for n in args:
        value = value * n
    return value
