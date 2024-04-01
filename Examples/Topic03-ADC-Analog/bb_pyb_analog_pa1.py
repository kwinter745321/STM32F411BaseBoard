# bb_pyb_analog_pa1.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20
#
from pyb import ADC, Pin
import time

# connect a wire between A1 and one of the potentiometers.
pot_pin = 'PA1'
# Connect a wire between B10 and a button.
USER_BUTTON_PIN = 'PB10'

pot = ADC(pot_pin)
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)

done = False
try:
    print("----------------")
    print("Program started.")
    print("* PA1 pin is wired to a 10k Potentiometer.")
    print("* Analog readings are 12 bits of accuracy (0-4095).")
    print("* Calculate the volts (knowing this is a 3.3 v MCU).\n")
    print("Press User button when ready to begin readings.")
    user_btn = 1
    
    while user_btn == 1:
        user_btn = user.value()
        #print("user: ",user_btn)
        time.sleep(.1)
        
    print("Press Control-c in Shell to exit.")
    while not done:
        reading = pot.read()
        value = (reading * 3.3) / 4095
        print(" Reading: %d Value: %.2f volts" % (reading,value))
        time.sleep(1)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    print('Finished.')
