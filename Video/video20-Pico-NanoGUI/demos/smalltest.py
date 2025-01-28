# smalltest.py
#
# Modified 28 January 2025
# By 2025 KW Services to support SSD1963 800X480 LCD Display.
# MIT License
# MicroPython v1.20.0 on 2023-04-26; Raspberry Pi Pico with RP2040
#
from color_setup import ssd
import time

drawpixel = ssd.drawPixel
color = bytearray((0, 255, 0))
start = time.ticks_ms()
for i in range (0, 480):  # filling pixel-by-pixel
    ssd.drawVLine(i, 0, 272, color)
    # for j in range (0, 271):
        # drawpixel(i, j, color)
time0 = time.ticks_ms() - start
print('DrawPixels: {} ms'.format(time0))
time.sleep_ms(2000)
