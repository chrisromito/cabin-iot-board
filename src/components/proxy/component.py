from machine import Pin
from settings import PROXY_ADAPTER, PROXY_PIN_ADAPTER, PROXY_QWIIC_ADAPTER, PROXY_TRIGGER_PIN, PROXY_ECHO_PIN
from .pin import PinAdapter
from .qwiic import QwiicAdapter
from components.shared import Buses


def get_adapter(buses: Buses):
    if PROXY_PIN_ADAPTER == PROXY_ADAPTER:
        return PinAdapter(
            trigger_pin=Pin(PROXY_TRIGGER_PIN),
            echo_pin=Pin(PROXY_ECHO_PIN)
        )
    return QwiicAdapter(buses.iic)


class Proxy:
    def __init__(self, buses: Buses):
        self.adapter = get_adapter(buses)
        self.is_ready = False

    async def setup(self):
        self.is_ready = await self.adapter.setup()
        return self.is_ready

    def get_distance(self):
        if not self.is_ready:
            return False
        return self.adapter.get_distance()

    async def async_get_distance(self):
        if not self.is_ready:
            return False
        return await self.adapter.async_get_distance()
