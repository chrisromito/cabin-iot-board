"""
Adapter for Sparkfun QWIIC HC-SR04 breakout
Adapted from source code here: https://github.com/sparkfun/Zio-Qwiic-Ultrasonic-Distance-Sensor
Product Page: https://www.sparkfun.com/products/17777

"""
from micropython import const
import uasyncio
from utime import sleep_ms

from utils.math_utils import scale
from utils.type_conversions import bytes_to_int


_DEFAULT_ADDRESS = const(0x00)
_OTHER_ADDRESS = const(0x08)
_ADDRESS_OPTIONS = [_DEFAULT_ADDRESS, _OTHER_ADDRESS]
_SLEEP = const(5)


class QwiicAdapter:
    """
    >>> from machine import I2C, Pin
    >>> iic = I2C(0, sda=Pin(23), scl=Pin(22))
    >>> proxy = QwiicProxy(iic)
    >>> proxy.get_distance()  # 60909
    """

    def __init__(self, iic, address=_DEFAULT_ADDRESS):
        self.iic = iic
        self.address = address
        self.is_ready = False
        self.distance = 0
        addresses = iic.scan()
        for option in addresses:
            if option in _ADDRESS_OPTIONS:
                self.address = option

    async def setup(self):
        self.is_ready = True
        return self.is_ready

    def read(self, n_bytes: int = 2) -> bytes:
        """
        >>> proxy = QwiicProxy( I2C(0, sda=Pin(23), scl=Pin(22)) )
        >>>
        :param int n_bytes:
        :return: bytes
        """
        return self.iic.readfrom(self.address, n_bytes)

    def write(self, value):
        return self.iic.writeto(
            self.address,
            bytearray([value])
        )

    def get_distance(self, n_bytes=2)-> int:
        self.write(0x01)
        sleep_ms(_SLEEP)
        distance = bytes_to_int(self.read(n_bytes))
        self.distance = distance
        return distance

    async def async_get_distance(self, n_bytes=2)-> int:
        self.write(0x01)
        await uasyncio.sleep_ms(_SLEEP)
        distance = bytes_to_int(self.read(n_bytes))
        self.distance = distance
        return distance
