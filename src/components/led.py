from machine import Pin, Signal
from settings import RED_LED, GREEN_LED, BLUE_LED


class Led:
    def __init__(self, pin_number: int):
        self.signal = Signal(Pin(pin_number, mode=Pin.OUT))
        self.is_ready = False

    async def setup(self):
        self.is_ready = True
        return True

    def on(self):
        return self.signal.on()

    def off(self):
        return self.signal.off()

    def update(self, turn_on=False):
        return (
            self.on() if turn_on
            else self.off()
        )


class Leds:
    def __init__(self):
        self.red = Led(RED_LED)
        self.green = Led(GREEN_LED)
        self.blue = Led(BLUE_LED)
        self.is_ready = False

    async def setup(self):
        if not self.is_ready:
            await self.red.setup()
            await self.green.setup()
            await self.blue.setup()
            self.is_ready = True
        return True

    def on(self):
        self.red.on()
        self.green.on()
        self.blue.on()

    def off(self):
        self.red.off()
        self.green.off()
        self.blue.off()
