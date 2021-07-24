from machine import Pin
from .pin import PinAdapter
from .qwiic import QwiicAdapter
from settings import BUTTON_ADAPTER, BUTTON_PIN_ADAPTER, BUTTON_QWIIC_ADAPTER, BUTTON_PIN
from components.shared import Buses


def get_adapter(buses: Buses):
    if BUTTON_PIN_ADAPTER == BUTTON_ADAPTER:
        return PinAdapter(Pin(BUTTON_PIN))
    return QwiicAdapter(buses.iic)


class Button:
    def __init__(self, buses: Buses, on_change=None):
        self.adapter = get_adapter(buses)
        self.on_change = on_change
        self.is_ready = False
        self._pressed = False

    async def setup(self):
        self.is_ready = await self.adapter.setup()
        return self.is_ready

    def is_pressed(self):
        if not self.is_ready:
            return False
        pressed = self.adapter.is_pressed()
        if self._pressed != pressed:
            self._pressed = pressed
            if self.on_change:
                self.on_change(self._pressed)
        self.adapter.clear()
        return pressed
