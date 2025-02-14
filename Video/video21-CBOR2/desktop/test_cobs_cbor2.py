# test_cobs_cbor2.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# Python 3.11.11
# conda gui311
#
import serial
import os
import time
import datetime
import pytz
from cobs_volts import send_msg, get_msg

import cbor2

#pip install keyboard
import keyboard

comport = "COM5"

ser = serial.Serial(port=comport, baudrate=38400, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=False, rtscts=0, dsrdtr=False)
#ser = serial.serial_for_url('loop://', timeout=1)  #desktop

if __name__ == '__main__':
    
    done = False
    print("CBOR2 Test from Desktop.")
    print("Starts waiting for data. ")
    print("Press keyboard 'd' to send hello message.")
    print("Press keyboard 's' to send data message.")
    print("Press keyboard 't' to send date message.")
    print("Press Control-c key to quit.")
    print("Note: hold down the desired key for ~1 sec.")
    cnt = 0
    while not done:

        data = get_msg(ser, 1)
        if data != b'':
            print("="*64)
            print("Received from STM32:",data,"length:",len(data) )
            obj = cbor2.loads(data)
            print("CBOR (decodes) loads:",obj)
            for b in obj:
                print("  Data: ",type(b), b)
            print("="*64)

        if keyboard.is_pressed('q'):
            exit()

        if keyboard.is_pressed('d'):
            t = b"hello"
            msg = [t]
            print("-"*64)
            s = cbor2.dumps(msg)  # s is a bytes object
            print("Sending message: ",msg)
            print("CBOR (Encode) dumps:",s,"length:",len(s) )
            send_msg(ser, s)
            print("-"*64)
        
        if keyboard.is_pressed('s'):
            m = b"hello"
            cnt += 1
            msg = [ m, cnt, True, 1.212]
            print("-"*94)
            s = cbor2.dumps(msg)  # s is a bytes object
            print("Sending message: ",msg)
            print("CBOR (Encode) dumps:",s,"length:",len(s) )
            send_msg(ser, s)
            print("-"*94)

        if keyboard.is_pressed('t'):
            m = b"hello"
            cnt += 1
            #dt = str(datetime.datetime.now())[11:19]
            #dt = str(datetime.datetime.now(pytz.utc))[11:19]
            #dt = datetime.datetime.now(pytz.utc)
            nyc_tz = pytz.timezone('America/New_York')
            dt = datetime.datetime.now().astimezone(nyc_tz)
            msg = [ m, cnt, True, 1.212, dt ]
            print("-"*114)
            s = cbor2.dumps(msg)  # s is a bytes object
            print("Sending message: ",msg)
            print("CBOR (Encode) dumps:",s,"length:",len(s) )
            send_msg(ser, s)
            print("-"*114)
    ser.close()
    
