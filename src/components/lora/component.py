from components.shared import BaseComponent, Buses
from components.lora.rylr_modules import Rylr
from components.lora.packet import Payload, payload_to_lora, Header
from utils.logger import log


class Lora:  # type: BaseComponent
    def __init__(self, buses: Buses):
        self.adapter = Rylr(buses.uart)

    async def setup(self):
        self.adapter.init()
        return True

    async def heartbeat(self):
        log.debug('Lora.heartbeat()')
        alive = self.adapter.heartbeat()
        log.debug('Lora.heartbeat? ' + str(bool(alive)))
        return bool(alive)

    async def write(self, data, address=0):
        return self.adapter.send(
            Payload(data, Header.this_device()).to_lora(),
            address
        )

    def receive(self):
        return self.adapter.receive()

