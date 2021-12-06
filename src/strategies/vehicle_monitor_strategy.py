"""
VehicleMonitorStrategy: Checks the proximity sensor's reading, if it gives anything
other than 0, for now, we're handing off to the vehicle_detected_strategy

"""

from strategies.strategy import BaseStrategy
from strategies.vehicle_detected_strategy import VehicleDetectedStrategy


class VehicleMonitorStrategy(BaseStrategy):
    async def start(self)-> bool:
        print('\n\n\n')
        print('VehicleMonitorStrategy.start()')
        component_map = self.context.component_map
        distance = await component_map.proxy.async_get_distance()
        print('distance:')
        print(str(distance))
        if distance:
            print('Adding VehicleDetectedStrategy to context.tasks')
            self.context.tasks.append(
                self.transition_to(
                    VehicleDetectedStrategy(context=self.context)
                )
            )
            return True
        return False
