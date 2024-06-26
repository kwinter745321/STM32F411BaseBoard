# bb_pyb_test_sdcard.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20 
#
from pyb import Pin
import os, sys
import time

# (1) Please copy the sdcard.py file to the BlackPill flash directory.

try:
    import sdcard
    print("Imported sdcard lib")
except:
    print("** Missing sdcard library.")
    print("   Please upload it to the BlackPill.")
    sys.exit(1)
finally:
    print()
    
# (2) Wire a connection between B10 and a button.
# (3) Make sure the four jumpers are inserted into the eight-pin SPI-2/SD Card
# (4) push a MicroSD card into the socket (gold fingers are on bottom.)

USER_BUTTON_PIN = 'PB10'
user = Pin(USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP)

#CD pullup to VCC with 10K e.g. btn3
WP = None
SCK = Pin('PB13')
MISO = Pin('PB14')
MOSI = Pin('PB15')
CS = Pin('PB12')
SPI_PORT = 2
# below configured SPI-2 for the sdcard
try:
    print("----------------")
    print("Program started (using the SD card).")
    print("* The SPI interface is using SPI-{} pins.".format(SPI_PORT))
    print("* - CS   is %s." % (CS) )
    print("* - SCK  is %s." % (SCK) )
    print("* - MISO is %s." % (MISO) )
    print("* - MOSI is %s." % (MOSI) )
    print("")
    sd = sdcard.SDCard(pyb.SPI(SPI_PORT), CS)
    pyb.mount(sd, '/sd')
    print("SD card mounted as /sd.")
except:
    print("** no SD card.")
    sys.exit(2)
finally:
    print()

done = False
mydir = "/sd"
try:
    prompt = "Press User button to list directory or Control-c in Shell to exit."
    print(prompt)
    while not done:
        user_btn = user.value()
        if user_btn == 0:
            print("Listing for {}.".format(mydir))
            time.sleep(0.5)
            files = os.listdir(mydir)
            for file in files:
                print(" --",file)
            print(prompt)
        time.sleep(0.2)
except KeyboardInterrupt:
    done = True
    print('Interrupted by Control-c.')
finally:
    print('Finished.')