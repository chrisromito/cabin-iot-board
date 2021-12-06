from micropython import const
# Gravity in m/s^2
GRAVITY_ACCELERATION = 9.80665

# Common numbers (save RAM by using constants)
# ################################################
ZERO = const(0)
TWO = const(2)
THREE = const(3)
FOUR = const(4)
FIVE = const(5)
SIX = const(6)
SIXTY = const(60)


MILLION = const(1000000)
THOUSAND = const(1000)
HUNDRED = const(100)
TEN = const(10)
ONE = const(1)
TENTH = 0.1
HUNDREDTH = 0.01
THOUSANDTH = 0.001
MILLIONTH = 10 ** -6
MAX_DUTY = const(1023)
