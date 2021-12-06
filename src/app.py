from uasyncio import gather, sleep_ms, sleep

from machine import deepsleep
from components.cameras.component import Camera
from components.fan import Fan
from components.led import Leds
from components.lora.component import Lora
from components.proxy.component import Proxy
from components.shared import Buses, ComponentMap
from components.thermometer.tmpxx import Thermometer
from settings import SLEEP_DURATION_MS
from strategies.boot_strategy import BootStrategy
from strategies.context import AppContext
from strategies.vehicle_monitor_strategy import VehicleMonitorStrategy
from strategies.temperature_regulator_strategy import TemperatureMonitorStrategy, TEMPERATURE_CORRECTION_OFF_TIME
from utils.logger import log


async def runtime():
    """
    runtime - Initializes the app, then calls `app.loop()` until it returns False
    :return:
    """
    log.debug('runtime()')
    app = App()
    keep_running = True
    while keep_running:
        keep_running = await app.loop()
    log.debug('runtime is done')
    countdown = 5
    while countdown > 0:
        log.debug('Deep sleep in ' + str(countdown) + ' seconds...')
        await sleep(1)
        countdown = countdown - 1
    return True


def after_runtime():
    """
    after_runtime: puts the device in a deep sleep so we can save energy
    :return:
    """
    log.debug('after_runtime()')
    deepsleep(SLEEP_DURATION_MS)


class App:
    def __init__(self):
        self.run = True
        self.buses = Buses()
        buses = self.buses
        self.component_map = ComponentMap(
            leds=Leds(),
            camera=Camera(buses),
            proxy=Proxy(buses),
            lora=Lora(buses),
            thermometer=Thermometer(),
            fan=Fan()
        )
        self.context = AppContext(BootStrategy(), self.component_map)
        self.temperature_context = AppContext(TemperatureMonitorStrategy(), self.component_map)

    async def loop(self):
        try:
            vehicle_detected = await self.context.start()
            temperature_correction = await self.temperature_context.start()
            tasks = (self.context.tasks + self.temperature_context.tasks)
            print('App.context.tasks.len? ' + str(len(tasks)))
            await gather(*tasks)
            if vehicle_detected or temperature_correction:
                self.context.strategy = VehicleMonitorStrategy(self.context)
                log.debug('App.loop -> vehicle_detected or temperature_correction')
                return True
            # elif temperature_correction and (not vehicle_detected):
            #     # If we haven't detected a vehicle, but we did need to do some temperature correction,
            #     # then sleep for a bit to give the fan more of a break. Deep sleep is only 3 seconds, but the fan
            #     # just ran for a couple of minutes. So we give the cheapy fans some breathing room (no pun intended)
            #     # for the sake of longevity
            #     log.debug('App.loop -> temperature_monitor_running')
            #     await sleep_ms(TEMPERATURE_CORRECTION_OFF_TIME)
            #     return True
            return False
        except Exception as err:
            log.error(err)
        log.debug('App.loop -> Nothing detected or corrected')
        return False
