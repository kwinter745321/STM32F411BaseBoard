# serial_loopback_test.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# python 3.10
#
# pip install pyserial
import serial
import time
from enum import Enum
import sys

# pip install keyboard
import keyboard

### Device Definitions ######################
SERIAL_PORT_SPEED = 38400
SERIAL_PORT = "COM6"

### Constants and Initialize variables ######
BUFFER_SIZE = 16

### SETUP ###################################
#serial = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_PORT_SPEED)  #desktop
serial = serial.serial_for_url('loop://', timeout=1)  #desktop

### Functions ###############################


### Main Loop ###############################
if __name__ == "__main__":
    done = False
    resp = bytearray(BUFFER_SIZE)
    cnt = 0
    dat = 0
    
    print("-"*70)
    print("Program started to transmit serial data.")
    print("-"*70)
    
    print("Press 's' to send message 'Control-c' to quit program. ")
    message = "hello"
    message = message.encode("utf-8")  #convert string to bytearray
    #message = "he" + chr(END_BYTE) + "llo" + chr(ESC_BYTE)

    try:
        while not done:
            
            if serial.in_waiting > 0:
                c = serial.read(1)
            
                dat = ord(c)
                resp = dat
                if resp != None:
                    print("Received: %d  %c" % (resp, resp) )

                
            if keyboard.is_pressed('s'):
                time.sleep(0.5)
                print("-"*85)
                print("Pressed 's'. Will send message:",message)
                
                cnt = serial.write(message)
                print("Sent %d bytes" % cnt)
                print("-"*85)

        time.sleep(0.1)
                
    except:
        print("Exception or Control-c entered.")
    finally:
        serial.close()
        print("Program finished")