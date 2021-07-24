"""
Adapter for Sparkfun QWIIC HC-SR04 breakout
Adapted from source code here: https://github.com/sparkfun/Zio-Qwiic-Ultrasonic-Distance-Sensor
Product Page: https://www.sparkfun.com/products/17777

"""
from micropython import const
import uasyncio

from utils.math_utils import scale


DEFAULT_ADDRESS = const(0x00)
OTHER_ADDRESS = const(0x08)
ADDRESS_OPTIONS = [DEFAULT_ADDRESS, OTHER_ADDRESS]
SLEEP = const(5)


class QwiicAdapter:
    """
    >>> from machine import I2C, Pin
    >>> iic = I2C(0, sda=Pin(23), scl=Pin(22))
    >>> proxy = QwiicProxy(iic)
    >>> raw_distance = proxy.read() # b'\x00\xed'
    >>> project_distance(raw_distance) # 60909
    >>> proxy.get_distance()  # 60909
    """

    def __init__(self, iic, address=DEFAULT_ADDRESS):
        self.iic = iic
        self.address = address
        self.is_ready = False
        self.distance = 0
        addresses = iic.scan()
        for option in addresses:
            if option in ADDRESS_OPTIONS:
                self.address = option

    async def setup(self):
        self.is_ready = True
        return ready

    def read(self, n_bytes: int = 2) -> bytes:
        """
        >>> proxy = QwiicProxy( I2C(0, sda=Pin(23), scl=Pin(22)) )
        >>>
        :param n_bytes:
        :return:
        """
        return self.iic.readfrom(self.address, n_bytes)

    def write(self, value):
        return self.iic.writeto(
            self.address,
            bytearray([value])
        )

    def get_distance(self, n_bytes=2):
        self.write(0x01)
        sleep_ms(SLEEP)
        distance = project_distance(self.read(n_bytes))
        self.distance = distance
        return distance

    async def async_get_distance(self, n_bytes=2):
        self.write(0x01)
        await uasyncio.sleep_ms(SLEEP)
        distance = project_distance(self.read(n_bytes))
        self.distance = distance
        return distance


def project_distance(iic_value: bytes) -> int:
    measured = parse(iic_value)
    last_pair = (0, 0)
    for proxy, mm in VALUE_MM_MAPPING:
        last_proxy, last_mm = last_pair
        if last_proxy <= measured <= proxy_value:
            # If the proxy distance given is somewhere between the last loop and the current
            # loop, scale it based on the respective min & maxes
            scale_value = scale(last_proxy, proxy, last_mm, mm)
            return scale_value(measured)
        last_pair = (proxy, mm)
    return 0


def parse(iic_value: bytes) -> int:
    iic_int = bytes_to_int(iic_value)
    left = iic_int << 8
    return left | iic_int


VALUE_MM_MAPPING = (
    # (i2c_value, actual_distance_mm)
    (34524, 0),
    (84468, 305),
    (164566, 610),
    (249584, 914),
    (324421, 1219),
    (432534, 1524),
    (506467, 1829),
    (596762, 2134)
)

# Testing
# ############
# from micropython import const
# DEFAULT_ADDRESS = const(0x00)
# from utime import sleep_ms
# from machine import I2C, Pin
#
#
# iic = I2C(0, sda=Pin(23), scl=Pin(22))
# a = DEFAULT_ADDRESS
#
#
# def read(n_bytes=2):
#     return iic.readfrom(a, n_bytes)
#
#
# def write(value):
#     return iic.writeto(a, bytearray([value]))
#
#
# def get_distance():
#     write(0x01)
#     sleep_ms(5)
#     return read()
