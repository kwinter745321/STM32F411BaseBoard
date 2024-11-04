# test_cobs_volts.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.24
#
import serial
import os
import time
import datetime
from cobs_volts import send_msg, get_msg

#pip install keyboard
import keyboard

comport = "COM5"

ser = serial.Serial(port=comport, baudrate=38400, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=False, rtscts=0, dsrdtr=False)
#ser = serial.serial_for_url('loop://', timeout=1)  #desktop

if __name__ == '__main__':
    
    done = False
    print("Volts COBS Test from Desktop.")
    print("Starts waiting for data. Press keyboard 's' to send message.")
    print("Press Control-c key to quit.")
    print("Note: hold down the 's' key for 1-1.5 secs.")
    while not done:

        data = get_msg(ser, 1)
        if data != b'':
            print("Received from STM32:",data)
        
        if keyboard.is_pressed('s'):
            time.sleep(0.4)
            msg = "hello"
            #msg = str(datetime.datetime.now())[11:]
            msgtx = msg.encode("utf-8")
            #msgtx = bytearray.fromhex('0102030405060708090A0B0C0D0E0F') 
            print("Sending to STM32:",msgtx)
            send_msg(ser, msgtx)

    ser.close()
    
