from uasyncio import sleep_ms

from micropython import const

from settings import FAN_MIN_THRESHOLD_CELSIUS, HEATING_MAX_THRESHOLD_CELSIUS
from utils.logger import log
from strategies.strategy import BaseStrategy


_SLEEP_MS = const(250)
# Let either temperature correction strategy run for 5 minutes before we re-assess temperature
_second_ms = 1000
_minute_ms = _second_ms * 60
_TEMPERATURE_CORRECTION_MS = _minute_ms * 5
TEMPERATURE_CORRECTION_OFF_TIME = _TEMPERATURE_CORRECTION_MS // 5


def requires_overheat_protection(temperature: float) -> bool:
    return temperature >= FAN_MIN_THRESHOLD_CELSIUS


def requires_freeze_protection(temperature: float) -> bool:
    return temperature <= HEATING_MAX_THRESHOLD_CELSIUS


class TemperatureMonitorStrategy(BaseStrategy):
    async def start(self)-> bool:
        temperature = self.context.component_map.thermometer.read()
        if requires_overheat_protection(temperature):
            log.debug('TemperatureMonitorStrategy engaging OverheatProtectionStrategy')
            self.context.tasks.append(
                self.transition_to(
                    OverheatProtectionStrategy()
                )
            )
            return True
        elif requires_freeze_protection(temperature):
            self.context.tasks.append(
                self.transition_to(
                    FreezeProtectionStrategy()
                )
            )
            log.debug('TemperatureMonitorStrategy engaging FreezeProtectionStrategy')
            return True
        # As long as the temperature is in a safe range we can exit/return
        log.debug('TemperatureMonitorStrategy does not need to engage')
        return False


class OverheatProtectionStrategy(BaseStrategy):
    async def start(self)-> bool:
        """
        Turn the fan on
        Wait 5 minutes
        Restart the loop
        :return:
        """
        self.context.component_map.fan.on()
        await sleep_ms(_TEMPERATURE_CORRECTION_MS)
        self.context.component_map.fan.off()
        return True


class FreezeProtectionStrategy(BaseStrategy):
    async def start(self)-> bool:
        return True
