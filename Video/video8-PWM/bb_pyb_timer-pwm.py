# bb_pyb_timer-pwm.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import Pin, Timer
import time

#Definitions---------
LED_PIN = "B3"
USER_BUTTON_PIN = 'PB10'
percent = 0

#Callback Routine
def cbLEDBrightness(event):
    global percent
    ch2.pulse_width_percent(percent)
    return


#Setup----------------
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
#Timer 2
tim2 = Timer(2, freq=1000, callback=cbLEDBrightness)
#Channel 2
ch2 = tim2.channel(2, Timer.PWM, pin=Pin(LED_PIN))



# Main Program--------
done = False
try:
    print("----------------")
    print("Program started to demonstrate PWM using a Timer.")
    print("* {} pin is wired to an LED indicator.".format(LED_PIN))
    print("* {} pin is wired to a push button.".format(USER_BUTTON_PIN))
    print("* Timer is {}.".format(tim2))
    print("* Channel is {}.\n".format(ch2))
    prompt = "Press User button to change brightness [or Control-c to exit.]"
    user_btn = 1
    print(prompt)
    print("LED brightness {}%.".format(percent))
    while not done:
        while user_btn == 1:
            user_btn = user.value()
            #print("user: ",user_btn)
            if user_btn == 0:
                user_btn = 1
                time.sleep(0.5)
                if percent >= 100:
                    percent = 0
                else:
                    percent = percent + 20
                print("LED brightness {}%.".format(percent))
        time.sleep(.1)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    ch2.pulse_width_percent(0)
    tim2.deinit()
    print('Finished.')
