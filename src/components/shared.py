from machine import Pin, I2C, UART

from constants import ONE
from settings import SDA, SCL, TX, RX, UART_BAUDRATE
from utils.logger import log


class Buses:
    def __init__(self):
        self.sda = Pin(SDA)
        self.scl = Pin(SCL)
        self.iic = I2C(0, sda=self.sda, scl=self.scl)
        self.uart = UART(ONE, UART_BAUDRATE)
        self.uart.init(baudrate=UART_BAUDRATE, tx=TX, rx=RX)


class AppInterface:
    buses: Buses


class BaseComponent:
    """
    ABC interface for components
    DO NOT inherit/extend this class. Use it as a reference instead
    """
    is_ready: bool

    async def setup(self):
        return self

    async def heartbeat(self) -> bool:
        return True


class ConnectionException(Exception):
    pass


class ComponentMap:
    def __init__(self, leds, camera, proxy, lora, thermometer, fan):
        self.leds = leds  # type: BaseComponent
        self.camera = camera  # type: BaseComponent
        self.proxy = proxy  # type: BaseComponent
        self.lora = lora  # type: BaseComponent
        self.thermometer = thermometer  # type: BaseComponent
        self.fan = fan  # type: BaseComponent
        self.is_ready = False

    @property
    def components(self) -> list[BaseComponent]:
        return (
            self.leds,
            self.camera,
            self.proxy,
            self.lora,
            self.thermometer,
            self.fan
        )

    async def setup(self):
        log.debug('ComponentMap.setup()')
        errors = []
        if self.is_ready:
            return True
        for component in self.components:
            name = component.__class__.__name__
            try:
                log.debug('Setup for: ' + str(name))
                await component.setup()
            except ConnectionException as err:
                errors.append(err)
            except Exception as err:
                log.debug('ComponentMap.setup -> error for ' + str(name))
                log.error(err)
                errors.append(err)
        if len(errors):
            for error in errors:
                raise error
        self.is_ready = True
        log.debug('ComponentMap.setup Complete')
        return True

    async def heartbeat(self):
        log.debug('ComponentMap.heartbeat()')
        healthy = True
        for component in self.components:
            try:
                component_healthy = await component.heartbeat()
                healthy = healthy and bool(component_healthy)
                if not healthy:
                    break
            except ConnectionException as err:
                raise err
            except Exception as err:
                log.debug('ComponentMap.heartbeat -> Caught an error:')
                log.error(err)
                raise err
        log.debug('ComponentMap.heartbeat -> healthy? ' + str(healthy))
        return healthy

