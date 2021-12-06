"""
Source: https://github.com/lemariva/uPySensors/blob/19c5e2a21d61dbb50bf3b1c9032789e816291720/hcsr04.py
"""
from machine import Pin, time_pulse_us
from micropython import const
from uasyncio import sleep
import utime

from constants import THOUSAND, MILLION


_DEFAULT_TIMEOUT = const(500 * 2 * 30)


async def sleep_us(us: float):
    return await sleep(us / MILLION)


def microsecond_to_cm(delta_microseconds: float) -> float:
    """
    Convert ticks_diff(ticks_us(), ticks_us()) -> centimeters
    - Divide by 2 to (the sound wave went "out" then "back")
    - Divide by the speed of sound in microseconds

    Speed of sound: 343.2 meters/second = 1cm/29.1 microseconds

    :param float delta_microseconds: Pulse duration (microseconds)
    :returns float:
    """
    return (delta_microseconds / 2) / 29.1


def micro_to_milli(micro):
    return micro / THOUSAND


class PinAdapter:
    """
    Driver to use the ultrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.
    The timeouts received listening to echo pin are converted to OSError('Out of range')
    """
    stable_us = 5
    echo_us = 10

    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin: Pin, echo_pin: Pin, echo_timeout_us: int = _DEFAULT_TIMEOUT):
        """
        :param trigger_pin: Output pin to send pulses
        :param echo_pin: (Input/Open-Drain) Receives pulse
        :param echo_timeout_us: Timeout in microseconds to listen to echo pin.
            Default is based in sensor limit range (4m)
        """
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = trigger_pin
        self.trigger.init(mode=Pin.OUT)
        self.trigger.value(0)
        # Init echo pin (in)
        self.echo = echo_pin
        self.echo.init(mode=Pin.OPEN_DRAIN)
        self.stable_ms = micro_to_milli(self.stable_us)
        self.echo_ms = micro_to_milli(self.echo_us)

    def get_pulse_microseconds(self) -> float:
        pulse_us = time_pulse_us(self.echo, self.echo_timeout_us)
        if pulse_us < 0:
            pulse_us = -1
        return pulse_us

    def _send_pulse_and_wait(self) -> float:
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `pulses_get()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0)  # Stabilize the sensor
        utime.sleep_ms(self.stable_ms)
        self.trigger.value(1)
        # Send a 10us pulse.
        utime.sleep_ms(self.echo_ms)
        self.trigger.value(0)
        return self.get_pulse_microseconds()

    async def _async_send_pulse_and_wait(self):
        """
        Same as _send_pulse_and_wait, but async
        """
        self.trigger.value(0)
        await sleep_us(self.stable_us)
        self.trigger.value(1)
        await sleep_us(self.echo_us)
        self.trigger.value(0)
        return self.get_pulse_microseconds()

    def get_distance(self) -> float:
        pulse_time = self._send_pulse_and_wait()
        return microsecond_to_cm(pulse_time)

    async def async_get_distance(self):
        pulse_time = await self._async_send_pulse_and_wait()
        return microsecond_to_cm(pulse_time)
