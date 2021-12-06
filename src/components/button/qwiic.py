"""
Adapter for Sparkfun QWIIC Button breakout
Adapted from source code here: https://github.com/sparkfun/Qwiic_Button_Py/blob/main/qwiic_button.py
Product Page: https://www.sparkfun.com/products/15931

"""
from micropython import const

from utils.type_conversions import bytes_to_int


DEFAULT_ADDRESS = const(0x6F)

DEVICE_ID = const(0x5D)

# Registers
# ###############
ID = const(0x00)
FIRMWARE_MINOR = const(0x01)
FIRMWARE_MAJOR = const(0x02)
BUTTON_STATUS = const(0x03)
INTERRUPT_CONFIG = const(0x04)
BUTTON_DEBOUNCE_TIME = const(0x05)
PRESSED_QUEUE_STATUS = const(0x07)
PRESSED_QUEUE_FRONT = const(0x08)
PRESSED_QUEUE_BACK = const(0x0C)
CLICKED_QUEUE_STATUS = const(0x10)
CLICKED_QUEUE_FRONT = const(0x11)
CLICKED_QUEUE_BACK = const(0x15)
LED_BRIGHTNESS = const(0x19)
LED_PULSE_GRANULARITY = const(0x1A)
LED_PULSE_CYCLE_TIME = const(0x1B)
LED_PULSE_OFF_TIME = const(0x1D)
I2C_ADDRESS = const(0x1F)


class QwiicAdapter:
    """
    >>> from components.button.component import Button
    >>> from components.button.qwiic import QwiicAdapter
    >>> from machine import I2C, Pin
    >>> iic = I2C(0, sda=Pin(23), scl=Pin(22))
    >>> adapter = QwiicAdapter(iic)
    >>> on_change = lambda status: print(f'Is Pressed? {status}')
    >>> button = Button(on_change=on_change)
    """

    def __init__(self, iic, address=DEFAULT_ADDRESS):
        self.iic = iic
        self.address = address
        self.is_ready = False

    def read(self, mem_address: bytes, num_bytes: int = 1) -> bytes:
        return self.iic.readfrom_mem(self.address, mem_address, num_bytes)

    async def setup(self):
        """
        Read from the ID register, if it comes back truthy we're good to go
        :return:
        """
        ready = DEVICE_ID == self.read(ID)
        self.is_ready = ready
        return ready

    def get_pressed_status(self) -> int:
        return bytes_to_int(
            self.iic.readfrom_mem(self.address, BUTTON_STATUS, 1)
        )

    def is_pressed(self):
        status = self.get_pressed_status() & ~0xFD
        was_pressed = status >> 1
        return bool(was_pressed)

    def clear(self):
        """
         Clear the is_pressed, has_been_clicked, and event_available
            bits of the BUTTON_STATUS register
        :return: None
        """
        value = self.get_pressed_status() & ~0x7
        self.iic.writeto_mem(self.address, BUTTON_STATUS, bytearray([value]))
