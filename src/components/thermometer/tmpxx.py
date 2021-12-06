from machine import ADC, Pin
from micropython import const

from components.shared import BaseComponent
from constants import ZERO
from settings import THERMOMETER_PIN
from utils.math_utils import scale
from utils.logger import log


_REF_VOLTS = 3.3
# See: https://docs.micropython.org/en/latest/esp32/quickref.html#adc-analog-to-digital-conversion
_ATTENUATION_MILLIVOLTS = const(1340)
_ATTENUATION = ADC.ATTN_2_5DB
_ADC_MAX = const(4095)
_DEFAULT_MV = const(1000)
_MIN_MV = const(100)
_MAX_MV = const(1750)
_MIN_C = const(-40)
_MAX_C = const(125)

adc_to_millivolts = scale(ZERO, _ADC_MAX, ZERO, _ATTENUATION_MILLIVOLTS)

millivolts_to_celsius = scale(_MIN_MV, _MAX_MV, _MIN_C, _MAX_C)


def adc_to_celsius(adc_value: int) -> float:
    return millivolts_to_celsius(
        adc_to_millivolts(adc_value)
    )


class Thermometer:  # type: BaseComponent
    """
    Interface for reading analog values from a
    TMP36 sensor
    """

    def __init__(self):
        self.adc = ADC(Pin(THERMOMETER_PIN))
        self.adc.atten(_ATTENUATION)
        self.is_ready = False

    async def setup(self):
        self.is_ready = True
        return self

    async def heartbeat(self):
        log.debug('Thermometer.heartbeat? ' + str(self.is_ready))
        return self.is_ready

    def read(self) -> float:
        """
        Get the current temperature in celsius
        :return: float
        """
        return adc_to_celsius(self.adc.read())
