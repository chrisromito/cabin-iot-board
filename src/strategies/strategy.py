class AbstractBaseStrategy:
    """
    Base Strategy to inherit from

    NOTE: You are expected to implement your own 'start' method if you need
    to do something when the context 'transitions_to' the given strategy
    """

    def __init__(self, context=None, **kwargs):
        self.context = context
        self._kwargs = kwargs

    async def transition_to(self, strategy):
        return await self.context.transition_to(strategy)


class BaseStrategy(AbstractBaseStrategy):
    can_sleep = False


class SleepStrategy(AbstractBaseStrategy):
    can_sleep = True
