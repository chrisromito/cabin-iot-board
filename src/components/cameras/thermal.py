"""
Product: AMG88xx, AMG8833, etc. using I2C protocol
Datasheet: https://mediap.industry.panasonic.eu/assets/custom-upload/Components/Sensors/Industrial%20Sensors/Infrared%20Array%20Sensor%20Grid-EYE/Grid-EYE_AMG88X_I2C%20communication.pdf

Source(s):
- Micropython AMG88xx: https://github.com/peterhinch/micropython-amg88xx/blob/master/amg88xx.py
- Circuitpython/Adafruit AMG88xx: https://github.com/adafruit/Adafruit_CircuitPython_AMG88xx/blob/main/adafruit_amg88xx.py

"""
from time import ticks_diff, ticks_ms

from machine import I2C
from micropython import const

from components.shared import Buses


EIGHT = const(8)
ONE = const(1)
ZERO = const(0)

# -- Device address
DEFAULT_ADDRESS = const(0x69)

# -- Registers
# Power: Section 21.1, register 0x00
POWER = const(0x00)
POWER_ON = const(0x00)
POWER_SLEEP = const(0x10)

# Reset: Section 21.2, register 0x01
RESET = const(0x01)
RESET_FLAG = const(0x30)
RESET_INITIAL = const(0x3F)

# Frame Rate: Section 21.3, register 0x02
FRAME_RATE = const(0x02)
FRAME_RATE_ONE = const(0x01)
FRAME_RATE_TEN = const(0x00)  # Default

# Interrupt control: Section 21.4, register 0x03
# Bit 0: EN
#    0 = INT output inactive. When in normal mode, this register becomes effective
#    1 = INT output active
# Bit 1: MOD
#    0 = Difference interrupt mode. Set temperature difference from the previous temp. value
#    1 = Absolute value interrupt mode. For setting temperature threshold??
INTERRUPT = const(0x03)
INTERRUPT_EN_ACTIVE = ONE
INTERRUPT_EN_INACTIVE = ZERO
INTERRUPT_MODE_DIFF = ZERO
INTERRUPT_MODE_ABSOLUTE = ONE

# Omitted sections 21.5 (status register) & 21.6 (status clear register) as they didn't seem relevant

THERMISTOR_REGISTER_LSB = const(0x0E)
PIXEL_REGISTER_START = const(0x80)
HEIGHT = const(8)
WIDTH = HEIGHT
PIXEL_TEMP_FACTOR = 0.25
THERMISTOR_FACTOR = 0.0625


def parse_temperature(buf: bytearray, index: int) -> float:
    """
    :param buf:
    :param index:
    :return:
    """
    raw_value = ((buf[index + 1] << 8) | buf[index]) & 0xfff
    if raw_value & 0x800:
        raw_value -= 0x1000
    return raw_value * PIXEL_TEMP_FACTOR


def wumbo_buffer_to_matrix(buf: bytearray) -> list[float]:
    """
    :param buf:
    :return: list[float]
    """
    temp = []
    for row in range(HEIGHT):
        for col in range(WIDTH):
            index = (row * HEIGHT + col) * 2
            try:
                temp.append(parse_temperature(buf, index))
            except Exception as err:
                print(err)
                temp.append(0.0)
    return temp


class Thermal:
    def __init__(self, iic: I2C, address=DEFAULT_ADDRESS):
        self.iic = iic
        self.address = address
        self.is_ready = False

    def write(self, register, value):
        return self.iic.writeto_mem(
            self.address,
            register,
            value if isinstance(value, bytearray) else bytearray([value])
        )

    def setup(self):
        if self.is_ready:
            return self
        # Power on (ie. not sleep mode), reset, disable interrupts, & set FPS
        temp = bytearray(1)
        temp[0] = POWER_ON
        self.write(POWER, temp)
        temp[0] = RESET_INITIAL
        self.write(RESET, temp)
        temp[0] = INTERRUPT_EN_INACTIVE
        self.write(INTERRUPT, temp)
        temp[0] = FRAME_RATE_TEN
        self.write(FRAME_RATE, temp)
        self.is_ready = True
        return self

    def read_all(self, buf=None):
        """
        Reads all of the pixel registers in one shot, then gives you the buffer back
        of all of its values
        :param Optional[bytearray] buf: None, or 128 byte bytearray
        :return: bytearray aka wumbo_buffer
        """
        if buf is None:
            buf = bytearray(HEIGHT * WIDTH * 2)
        self.iic.readfrom_mem_into(self.address, PIXEL_REGISTER_START, buf)
        return buf

    def read_all_to_matrix(self, buf=None) -> list[float]:
        return wumbo_buffer_to_matrix(self.read_all(buf))

    def get_device_temperature(self) -> float:
        buf = bytearray(2)
        self.iic.readfrom_mem_into(self.address, THERMISTOR_REGISTER_LSB, buf)
        raw = ((buf[1] << 8) | buf[0]) & 0xFFF
        if raw & 0x800:
            raw = -(raw & 0x7FF)
        return float(raw) * THERMISTOR_FACTOR


def get_register(iic: I2C, address, register, length: int = EIGHT) -> bytes:
    return iic.readfrom_mem(address, register, length)


def write_register(iic: I2C, address, register):
    def _write_register(value):
        write_value = value if isinstance(value, bytearray) else bytearray([value])
        return iic.writeto_mem(address, register, write_value)

    return _write_register


def test_camera_functionality():
    from time import sleep
    thermal = Thermal(Buses().iic)
    print('Starting thermal cam test')
    print('Setting up camera...')
    thermal.setup()
    sleep(1)
    print('Testing 20 sequential snapshots...')
    test_buf = bytearray(8 * 8 * 2)
    matrix_start = ticks_ms()
    for _ in range(20):
        thermal.read_all_to_matrix(test_buf)
    matrix_ms = ticks_diff(ticks_ms(), matrix_start)
    print('20 images taken in ' + str(matrix_ms) + ' milliseconds')
    print('Testing device thermometer...')
    start = ticks_ms()
    temp = thermal.get_device_temperature()
    temp_ms = ticks_diff(ticks_ms(), start)
    print('Device is ' + str(temp) + 'C')
    print('Temperature read took ' + str(temp_ms) + ' milliseconds')
