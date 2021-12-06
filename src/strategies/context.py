from components.shared import ComponentMap
from settings import FAN_MIN_THRESHOLD_CELSIUS, HEATING_MAX_THRESHOLD_CELSIUS
from strategies.strategy import BaseStrategy


class AppContext:
    """
    App Context helps provide a reference to an instance of a Strategy subclass.
    The Strategy will determine how actions are handled & what to do next.

    For example:
    - BootStrategy handles initial setup
    """

    def __init__(self, strategy: BaseStrategy, component_map: ComponentMap, tasks=None):
        self.strategy = strategy  # type: BaseStrategy
        self.component_map = component_map  # type: ComponentMap
        self.tasks = tasks or []  # type: list

    async def start(self)-> bool:
        self.tasks = []
        return await self.transition_to(self.strategy)

    async def transition_to(self, strategy: BaseStrategy)-> bool:
        self.strategy = strategy
        self.strategy.context = self
        if hasattr(self.strategy, 'start'):
            return await self.strategy.start()
        return False

