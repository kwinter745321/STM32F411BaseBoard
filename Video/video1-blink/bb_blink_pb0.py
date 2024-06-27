# bb_blink_pb0.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import Pin
import time

led = Pin("PB0", Pin.OUT)

print("Blink PB0")
while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
