from components.shared import Buses, BaseComponent
from utils.logger import log
from components.cameras.thermal import Thermal


class Camera:  # type: BaseComponent
    def __init__(self, buses: Buses):
        self.thermal = Thermal(buses.iic)
        self.is_ready = False

    async def setup(self):
        log.debug('Camera.setup()')
        self.thermal.setup()
        self.is_ready = True
        return True

    async def heartbeat(self):
        log.debug('Camera -> heartbeat()')
        try:
            self.thermal.get_device_temperature()
            log.debug('Camera -> heartbeat: True')
            return True
        except Exception as err:
            log.error(err)
            log.debug('Camera -> heartbeat: False')
            return False

    def get_temperature_matrix(self) -> list[float]:
        return self.thermal.read_all_to_matrix()

    def get_ambient_temperature(self) -> float:
        try:
            return self.thermal.get_device_temperature()
        except Exception as err:
            log.error(err)
        return 0.0
