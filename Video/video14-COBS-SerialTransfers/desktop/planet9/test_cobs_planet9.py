# test_mcobs_planet9.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# Python 3.9
#
import serial
import os
import time
import datetime

#pip install keyboard
import keyboard

from cobs_planet9 import send_msg, get_msg

ser = serial.Serial(port='COM5', baudrate=38400, bytesize=8, parity='N', stopbits=1,timeout=1, xonxoff=False, rtscts=0, dsrdtr=False)
#ser = serial.serial_for_url('loop://', timeout=1)  #desktop

if __name__ == '__main__':

    done = False
    print("Planet9 COBS Test from desktop.")
    print("Starts waiting for data. Press keyboard 's' to send message.")
    print("Press Control-c key to quit.")
    print("Note: Hold down the 's' key for 1-1.5 secs.")

    while not done:
        
        data = get_msg( serialport=ser, timeout_ms=1, verbose=False)
        if data != b'':
            print("Received:",data)

        if keyboard.is_pressed('s'):
            time.sleep(0.5)
            msg = "hello"
            #msg = str(datetime.datetime.now())[11:]
            message = msg.encode("utf-8")
            print ("Message Sent= ", message)
            send_msg(  serialport=ser, msg=message, verbose=False)

    ser.close()