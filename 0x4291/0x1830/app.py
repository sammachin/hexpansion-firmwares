import app
import neopixel
import asyncio
from patterns.rainbow import RainbowPattern
from machine import Pin


class RainbowUK(app.App):
    def __init__(self, config=None):
        self.config = config
        config.pin[3].init(drive=Pin.DRIVE_3)
        self.leds = neopixel.NeoPixel(config.pin[3], 78)
        self.brightness = 0.1
        self.pattern = RainbowPattern()

        self.button_a = config.pin[1]
        self.button_a.init(pull=Pin.PULL_UP)
        self.button_a.irq(self.dimmer)

        self.button_b = config.pin[0]
        self.button_b.init(pull=Pin.PULL_UP)
        self.button_b.irq(self.brighter)

    def dimmer(self):
        self.brightness -= 0.05
        if self.brightness <= 0:
            self.brightness = 0

    def brighter(self):
        self.brightness += 0.05
        if self.brightness >= 0.2:
            self.brightness = 0.2

    def update(self, delta=None):
        self.minimise()

    async def background_task(self):
        while True:
            frame = self.pattern.next()
            for i, val in enumerate(frame*7):
                if i >= 78:
                    break
                self.leds[i] = tuple(int(c * self.brightness) for c in val)
            self.leds.write()
            await asyncio.sleep(1/self.pattern.fps)

__app_export__ = RainbowUK
