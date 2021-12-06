"""
BootStrategy: Calls the 'setup' and 'heartbeat' methods on the `component_map`.

Ensures 2 things are true:
- Components are initialized
- Makes sure they're all alive & we can interface with them

As long as the above 2 conditions are True, it will hand off to the VehicleMonitorStrategy
   to begin... monitoring for vehicles

Otherwise, it will hand off to the OSOF Strategy because
that means the app failed the first step and we're SOL
"""
from utils.logger import log

from strategies.strategy import BaseStrategy, SleepStrategy
from strategies.vehicle_monitor_strategy import VehicleMonitorStrategy


class BootStrategy(BaseStrategy):
    async def start(self):
        print('BootStrategy.start()')
        heartbeat = await self.setup()
        leds = self.context.component_map.leds
        log.debug('BootStrategy -> heartbeat? ' + str(heartbeat))
        if heartbeat:
            await leds.heartbeat()
            print('BootStrategy is transitioning to VehicleMonitorStrategy')
            return await self.transition_to(
                VehicleMonitorStrategy()
            )
        else:
            await leds.error_sequence()
            print('BootStrategy failed to get a heartbeat, transitioning to SleepStrat')
            return False

    async def setup(self):
        print('BootStrategy.setup()')
        component_map = self.context.component_map
        leds = component_map.leds
        try:
            await component_map.setup()
            heartbeat = await component_map.heartbeat()
            return heartbeat
        except Exception as err:
            log.debug('BootStrategy.setup failed =(')
            log.error(err)
            await leds.error_sequence()
            raise err
