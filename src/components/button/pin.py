"""
Adapter for momentary-push Button components connected to GPIO pins
This assumes that the pin status changes such that:
    - LOW = not pressed
    - High = pressed
"""
from machine import Pin


class PinAdapter:
    def __init__(self, pin):
        self.pin = pin
        self.pin.init(mode=Pin.IN, pull=Pin.PULL_UP)
        self.is_ready = False

    def clear(self):
        pass

    async def setup(self):
        self.is_ready = True
        return True

    def is_pressed(self):
        return self.pin.value()
