# bb_pwm_quick-look.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import Pin, Timer
import time

#Definitions---------
LED_PIN = "B3"

#Setup----------------
#LED
p = Pin(LED_PIN) # utilises TIM2, CH2
#Timer 2
tim2 = Timer(2, freq=1000)
#Channel 2
ch2 = tim2.channel(2, Timer.PWM, pin=p)

# Main Program--------
for r in range(0,100,10):
    ch2.pulse_width_percent(r)
    time.sleep(0.5)
    print(r)
#Turn off the LED
ch2.pulse_width_percent(0)    
tim2.deinit()
