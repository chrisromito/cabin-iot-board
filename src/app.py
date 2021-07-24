from gc import collect
from machine import Pin, I2C, UART
from uasyncio import get_event_loop, run, sleep
from utime import time
from typing import List, Optional, Union, Any

from constants import ONE, TWO, ZERO
from components.shared import Buses
from components.button.component import Button
from components.camera import Camera
from components.led import Leds
from components.proxy.component import Proxy
from settings import PROXY_DISTANCE_THRESHOLD_CM, SLEEP_DURATION_MS
from utils.logger import Logger


def runtime():
    return run(_run_forever())


async def _run_forever():
    app = App()
    try:
        await app.setup()
    except Exception as err:
        app.logger.error(err)
        app.stop()
    await app.run_forever()


class App:
    def __init__(self):
        self.run = True
        self.buses = Buses()
        self.logger = Logger()
        self.button = None
        self.proxy = None
        self.leds = None
        self.camera = None

    def stop(self):
        self.run = False

    async def run_forever(self):
        while self.run:
            try:
                collect_after = await self.loop()
                self.leds.off()
                if collect_after:
                    collect()
            except Exception as err:
                try:
                    await self.handle_error(err)
                except Exception as fuck:
                    print('Error handler threw this error!!!!11!', fuck)

    async def setup(self):
        buses = self.buses
        # noinspection PyTypeChecker
        self.button = Button(buses)
        await self.button.setup()
        # noinspection PyTypeChecker
        self.proxy = Proxy(buses)
        await self.proxy.setup()
        self.leds = Leds()
        await self.leds.setup()
        # noinspection PyTypeChecker
        self.camera = Camera(buses)
        await self.camera.setup()
        return True

    async def loop(self):
        collect_after_this = False
        distance = await self.proxy.get_distance()
        is_close_enough = PROXY_DISTANCE_THRESHOLD_CM >= distance
        if is_close_enough or self.button.is_pressed():
            collect_after_this = await handle_photo(self)
        return collect_after_this

    async def handle_error(self, exception: Exception):
        self.logger.error(exception)
        self.leds.red.on()
        await sleep(6)


async def handle_photo(app: App):
    collect_after_this = False
    app.leds.blue.on()
    if app.camera.take_photo():
        collect_after_this = True
        try:
            photo_bytes = app.camera.read_photo_from_buffer()
            write_photo(photo_bytes)
            app.leds.green.on()
            # Green LED lets us know that the image was written successfully
            await sleep(5)
        except Exception as err:
            print('Error while writing photo (read went smoothly)', err)
        finally:
            # Always reset the camera after we successfully take a picture
            app.camera.reset()
    app.leds.blue.off()
    return collect_after_this


def write_photo(photo_bytes: List[int]):
    file_name = 'photo_' + str(time()) + '.jpg'
    with open(file_name, 'wb') as img:
        img.write(
            bytearray(photo_bytes)
        )
