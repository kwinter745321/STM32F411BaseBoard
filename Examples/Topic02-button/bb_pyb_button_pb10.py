# bb_pyb_button_pb10.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import Pin, LED
import time

# Builtin LED on the BlackPill.
BUILTIN_LED_NUM = 1
# the Builtin LED
led = LED(BUILTIN_LED_NUM)
led.off()

# Connect a wire between B10 and a button
KEY_BTN_PIN = 'PB10'
# Builtin Key user-definable button
key = Pin(KEY_BTN_PIN, Pin.IN, Pin.PULL_UP)

try:
    print("----------------")
    print("Program started.")
    print("* Builtin LED at {}.".format(led))
    print("* User button defined at {}.".format(key))
    print("\n")
    print("Press User button or Control-c in Shell to exit.")
    done = False
    while not done:
        key_btn = key.value()   # returns one or zero.
        #print("key_btn:",key_btn)
        if key_btn == 0:
            led.on()
            time.sleep(0.5)
        led.off()
        time.sleep(0.5)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    led.off()
    print('Finished.')
