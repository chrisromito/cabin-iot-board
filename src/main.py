import gc
from uasyncio import run
from app import runtime, after_runtime
gc.enable()

try:
    run(runtime())
    after_runtime()
except KeyboardInterrupt:
    pass
except Exception as err:
    print(err)
    after_runtime()
