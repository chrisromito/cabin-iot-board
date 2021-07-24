from functools import wraps, partial


def make_async(fn):
    """
    Async decorator (make a sync function async)
    >>> from utils import make_async
    >>> from time import sleep
    >>> @make_async
    >>> def my_async_sleep(seconds):
    >>>     sleep(seconds)
    """
    @wraps(fn)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        # noinspection PyArgumentList
        partial_fn = partial(fn, *args, **kwargs)
        return await loop.run_in_executor(executor, partial_fn)

    return run
