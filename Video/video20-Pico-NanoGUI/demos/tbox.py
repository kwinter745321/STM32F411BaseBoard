# tbox.py Test/demo of Textbox widget for nano-gui
#
# Modified 28 January 2025
# By 2025 KW Services to support SSD1963 800X480 LCD Display.
# MIT License
# MicroPython v1.20.0 on 2023-04-26; Raspberry Pi Pico with RP2040
#
# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2020 Peter Hinch

# Usage:
# import gui.demos.tbox

# Initialise hardware and framebuf before importing modules.
from color_setup import ssd  # Create a display instance

from gui.core.nanogui import refresh
from gui.core.writer import CWriter

import uasyncio as asyncio
from gui.core.colors import *
#import gui.fonts.arial10 as arial10
import gui.fonts.font10 as font10
from gui.widgets.label import Label
from gui.widgets.textbox import Textbox

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

# Args common to both Textbox instances
# Positional
pargs = (2, 2, 124, 7)  # Row, Col, Width, nlines

# Keyword
tbargs = {
    "fgcolor": YELLOW,
    "bdcolor": RED,
    "bgcolor": DARKGREEN,
}


async def wrap(wri):
    s = """The textbox displays multiple lines of text in a field of fixed dimensions. \
Text may be clipped to the width of the control or may be word-wrapped. If the number \
of lines of text exceeds the height available, scrolling may be performed \
by calling a method.
"""
    tb = Textbox(wri, *pargs, clip=False, **tbargs)
    tb.append(s, ntrim=100, line=0)
    refresh(ssd)
    while True:
        await asyncio.sleep(1)
        if not tb.scroll(1):
            break
        refresh(ssd)


async def clip(wri):
    ss = (
        "clip demo",
        "short",
        "longer line",
        "much longer line with spaces",
        "antidisestablishmentarianism",
        "line with\nline break",
        "Done",
    )
    tb = Textbox(wri, *pargs, clip=True, **tbargs)
    for s in ss:
        tb.append(s, ntrim=100)  # Default line=None scrolls to show most recent
        refresh(ssd)
        await asyncio.sleep(1)


async def main(wri):
    await wrap(wri)
    await clip(wri)


def test():
    refresh(ssd, True)  # Initialise and clear display.
    CWriter.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
    wri = CWriter(ssd, font10, verbose=False)
    wri.set_clip(True, True, False)
    asyncio.run(main(wri))


test()
