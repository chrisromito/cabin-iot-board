from uasyncio import sleep_ms

from machine import Pin, Signal

from components.shared import BaseComponent
from settings import FAN_PIN
from utils.logger import log


class Fan:  # type: BaseComponent
    def __init__(self):
        self.is_ready = False
        self.signal = Signal(Pin(FAN_PIN, Pin.OUT))

    async def setup(self):
        self.is_ready = True
        return self

    async def heartbeat(self):
        log.debug('Fan.heartbeat()')
        try:
            self.signal.on()
            await sleep_ms(200)
            self.signal.off()
            log.debug('Fan.heartbeat? True')
            return True
        except Exception as err:
            log.debug('Fan.heartbeat? False')
            log.error(err)
            return False
