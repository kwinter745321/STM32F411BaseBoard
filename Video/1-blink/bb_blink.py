# bb_blink.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import LED
import time

led = LED(1)

print("Blink LED(1) which is pin PC13")
while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
