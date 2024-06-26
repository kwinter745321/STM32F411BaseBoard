# bb_pyb_timer-pwm_b3.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import Pin, Timer
import time

# connect a wire between B3 and an LED indicator.
pwm_pin = 'PB3'
# Connect a wire between B10 and a button.
USER_BUTTON_PIN = 'PB10'
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
# Define a Timer and Channel for PWM
tim2 = Timer(2, freq=1000)
ch2 = tim2.channel(2, Timer.PWM, pin=Pin(pwm_pin))

done = False
try:
    print("----------------")
    print("Program started to demonstrate PWM using a Timer.")
    print("* {} pin is wired to an LED indicator.".format(pwm_pin))
    print("* Timer is {}.".format(tim2))
    print("* Channel is {}.\n".format(ch2))
    prompt = "Press User button to begin or Control-c to exit."
    user_btn = 1
    print(prompt)
    while not done:
        while user_btn == 1:
            user_btn = user.value()
            #print("user: ",user_btn)
            if user_btn == 0:
                for r in range(20,100,20):
                    ch2.pulse_width_percent(r)
                    time.sleep(0.1)
                    print("LED brightness {}%.".format(r))
                    time.sleep(1)
                ch2.pulse_width_percent(0)
                print(prompt)
                user_btn = 1
        time.sleep(.1)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    ch2.pulse_width_percent(0)
    tim2.deinit()
    print('Finished.')
