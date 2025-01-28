# round.py Test/demo of scale widget for nano-gui on round gc9a01 screen
#
# Modified 28 January 2025
# By 2025 KW Services to support SSD1963 800X480 LCD Display.
# MIT License
# MicroPython v1.20.0 on 2023-04-26; Raspberry Pi Pico with RP2040
#
# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2024 Peter Hinch

# Usage:
# import gui.demos.round

# Initialise hardware and framebuf before importing modules.
# Uses asyncio and also the asynchronous do_refresh method if the driver
# supports it.

from color_setup import ssd  # Create a display instance

from gui.core.nanogui import refresh
from gui.core.writer import CWriter

import uasyncio as asyncio
from gui.core.colors import *
#import gui.fonts.arial10 as arial10
import gui.fonts.font10 as font10
from gui.widgets.label import Label
from gui.widgets.scale import Scale

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHTRED = (140, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
LIGHTGREEN = (0, 100, 0)
DARKGREEN = (0, 80, 0)
DARKBLUE = (0, 0, 90)
WHITE = (255, 255, 255)

# COROUTINES
async def radio(scale):
    cv = 88.0  # Current value
    val = 108.0  # Target value
    while True:
        v1, v2 = val, cv
        steps = 200
        delta = (val - cv) / steps
        for _ in range(steps):
            cv += delta
            # Map user variable to -1.0..+1.0
            scale.value(2 * (cv - 88) / (108 - 88) - 1)
            await asyncio.sleep_ms(200)
        val, cv = v2, v1


async def default(scale, lbl):
    cv = -1.0  # Current
    val = 1.0
    while True:
        v1, v2 = val, cv
        steps = 400
        delta = (val - cv) / steps
        for _ in range(steps):
            cv += delta
            scale.value(cv)
            lbl.value("{:4.3f}".format(cv))
            if hasattr(ssd, "do_refresh"):
                # Option to reduce asyncio latency
                await ssd.do_refresh()
            else:
                # Normal synchronous call
                refresh(ssd)
            await asyncio.sleep_ms(250)
        val, cv = v2, v1


def test():
    def tickcb(f, c):
        if f > 0.8:
            return RED
        if f < -0.8:
            return BLUE
        return c

    def legendcb(f):
        return "{:2.0f}".format(88 + ((f + 1) / 2) * (108 - 88))

    refresh(ssd, True)  # Initialise and clear display.
    CWriter.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
    wri = CWriter(ssd, font10, GREEN, BLACK, verbose=False)
    wri.set_clip(True, True, False)
    scale1 = Scale(wri, 64, 64, width=124, legendcb=legendcb, pointercolor=RED, fontcolor=YELLOW)
    asyncio.create_task(radio(scale1))

    lbl = Label(wri, 180, 64, 50, bgcolor=DARKGREEN, bdcolor=RED, fgcolor=WHITE)
    # do_refresh is called with arg 4. In landscape mode this splits screen
    # into segments of 240/4=60 lines. Here we ensure a scale straddles
    # this boundary
    scale = Scale(
        wri, 140, 64, width=124, tickcb=tickcb, pointercolor=RED, fontcolor=YELLOW, bdcolor=CYAN
    )
    asyncio.run(default(scale, lbl))


test()
