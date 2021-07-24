from machine import Pin, I2C, UART
from constants import ZERO, ONE, TWO
from settings import SDA, SCL, TX, RX, RED_LED, GREEN_LED, BLUE_LED, UART_BAUDRATE, SLEEP_DURATION_MS


class Buses:
    def __init__(self):
        sda = Pin(SDA)
        scl = Pin(SCL)
        self.iic = I2C(0, sda=sda, scl=scl)
        self.uart = UART(ONE, UART_BAUDRATE)


class AppInterface:
    buses: Buses
