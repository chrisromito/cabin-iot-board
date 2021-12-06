from math import pi, sin

from machine import Pin, PWM
from micropython import const
from uasyncio import sleep_ms

from settings import STATUS_LED, LOW_POWER_LED, VEHICLE_LED
from utils.logger import log


# Try to keep sequences around 3000 ms
SEQUENCE_DURATION_MS = const(3000)
_HEARTBEAT_DURATION_MS = const(1542)


class Led:
    def __init__(self, pin_number: int):
        self.pin = Pin(pin_number, mode=Pin.OUT)

    def on(self):
        return self.pin.on()

    def off(self):
        return self.pin.off()

    def update(self, turn_on=False):
        return (
            self.on() if turn_on
            else self.off()
        )


class Leds:
    def __init__(self):
        self.board = Led(13)
        self.status = Led(STATUS_LED)
        self.low_power = Led(LOW_POWER_LED)
        self.vehicle = Led(VEHICLE_LED)
        self.is_ready = False

    async def heartbeat(self):
        log.debug('Leds.heartbeat()')
        try:
            await heartbeat_sequence(self)
        except Exception as err:
            log.debug('Leds.heartbeat? False')
            log.error(err)
            self.board.on()
            return False
        self.board.on()
        log.debug('Leds.heartbeat? True')
        return True

    async def error_sequence(self):
        log.debug('Leds.error_sequence()')
        self.board.off()
        try:
            await error_sequence(self)
        except Exception as err:
            log.error(err)
            return False
        self.board.on()
        return True

    async def setup(self):
        self.is_ready = True
        return True

    def on(self):
        for led in self.leds:
            led.on()

    def off(self):
        for led in self.leds:
            led.off()

    @property
    def leds(self):
        return (
            self.status,
            self.low_power,
            self.vehicle,
        )


async def error_sequence(leds: Leds):
    """
    error_sequence: 30 flashes, with a TOTAL on-off cycle of 100ms
        ( on: 50ms, off: 50ms ) * 30
        (50 + 50) * 10
        3,000ms = 3 second
    :param leds:
    :return:
    """
    for _ in range(30):
        await flash(leds, 100)


async def heartbeat_sequence(leds: Leds):
    """
    Healthy heartbeat sequence is like:
        # Thud Thud Rest Thud Thud Rest Thud Thud Rest
        Thud = T = (on: 25, off: 25) = 50ms
        Rest = R = (off: 200ms) = 200ms
        (T + T + R) * 10
        (50 + 50 + 200) * 10
        3,000ms = 3 seconds
    :param leds:
    :return:
    """
    for _ in range(10):
        await flash(leds, 50)  # thud
        await flash(leds, 50)  # thud
        await sleep_ms(200)  # rest
    return


async def flash(leds: Leds, ms: int):
    leds.status.on()
    duration = int(ms / 2)
    await sleep_ms(duration)
    leds.status.off()
    await sleep_ms(duration)


async def pulse(pwm, duration, pulse_range=20):
    # noinspection PyTypeChecker
    for i in range(pulse_range):
        pwm.duty(
            int(sin(i / 10 * pi) * 500 + 500)
        )
        await sleep_ms(duration)
