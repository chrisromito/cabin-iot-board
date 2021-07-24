from math import degrees, pi, radians

from constants import (
    GRAVITY_ACCELERATION, MILLION, THOUSAND, HUNDRED, TEN, ONE,
    TENTH, HUNDREDTH, THOUSANDTH, MILLIONTH,
    SIXTY
)
from utils.math_utils import Number


class Metric:
    scale = {
        'kilo': THOUSAND,
        'hecto': HUNDRED,
        'deca': TEN,
        'base': ONE,
        'deci': TENTH,
        'centi': HUNDREDTH,
        'milli': THOUSANDTH,
        'micro': MILLIONTH
    }

    def __init__(self, value, factor='base'):
        self.value = value
        self.factor = self.scale.get(factor, ONE)

    def is_base(self):
        return self.factor == ONE

    def to_base(self):
        return self.value * self.factor

    def from_base(self):
        return self.value / self.factor

    def convert(self, factor_key):
        factor = self.scale.get(factor_key, ONE)
        return self.to_base() / factor


# Time
# ##########
def milli_to_base(milli: Number) -> Number:
    return milli / THOUSANDTH


def base_to_milli(base: Number) -> Number:
    return base * THOUSANDTH


def micro_to_base(micro: Number) -> Number:
    return micro / MILLION


def base_to_micro(base: Number) -> Number:
    return base * MILLION


# Angles
# #############

def degrees_to_rad(n):
    return radians(n)


def rad_to_degrees(n):
    return degrees(n)


def rpm_to_radsec(n):
    rad_per_minute = n * 2 * pi
    return rad_per_minute * SIXTY


# Acceleration
# #############

def gravity_to_mss(n):
    return n * GRAVITY_ACCELERATION


def mss_to_gravity(n):
    return n / GRAVITY_ACCELERATION


# Distance
# #############
_INCH_RATIO: float = 2.54
_INCH_METER_RATIO: float = 2.54 / HUNDRED


def inch_to_meter(inch):
    return inch * _INCH_METER_RATIO


def meter_to_inch(meter):
    return meter / _INCH_METER_RATIO


def inch_to_metric(inch):
    return Metric(
        inch_to_meter(inch)
    )
