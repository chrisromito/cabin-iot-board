"""
VehicleDetectedStrategy - Oh you detected a vehicle? I'll grab a snapshot, introspect it,
    and send it to the LoRa gateway if it's for sure a vehicle

This then uses _kwargs['vehicle_monitor'] to restart the VehicleMonitorStrategy

NOTE: Right now, we're saying everything is a vehicle, so we just take a snapshot & send it =D
"""
from micropython import const
from uasyncio import sleep_ms
from utils.logger import log
import ujson

from strategies.strategy import BaseStrategy

_VEHICLE_DETECTED_SNAPSHOT_DELAY_MS = const(250)


class VehicleDetectedStrategy(BaseStrategy):
    async def start(self)-> bool:
        try:
            print('\n\n\n')
            log.debug('VehicleDetectedStrategy.start()')
            component_map = self.context.component_map
            camera = component_map.camera
            log.debug('Setting up payload...')
            temperature_matrix = list(map(int, camera.get_temperature_matrix()))
            payload_values = [
                component_map.proxy.get_distance(),
                camera.get_ambient_temperature()
            ] + temperature_matrix
            log.debug('Sending payload...')
            await component_map.lora.write(payload_values)
            log.debug('VehicleDetectedStrategy successfully sent a LoRa payload')
            log.debug('Doing some blinky stuff then handing back to vehicle_monitor_strategy')
            led = component_map.leds.vehicle
            led.on()
            await sleep_ms(_VEHICLE_DETECTED_SNAPSHOT_DELAY_MS)
            led.off()
            return True
        except Exception as err:
            log.debug('VehicleDetectedStrategy.start -> threw an Exception:')
            log.error(err)
            raise err
