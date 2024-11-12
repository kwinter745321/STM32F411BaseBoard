# test_pyserial_pickle.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# Python 3.9, pySerial, keyboard
#
import serial
import gc
import time

import pickle

#pip install keyboard
import keyboard

comport = "COM4"

ser = serial.Serial(port=comport, baudrate=38400, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=False, rtscts=0, dsrdtr=False)
#ser = serial.serial_for_url('loop://', timeout=1)  #desktop

def is_ascii(data):
    try:
        data.decode('ascii')
        return True
    except UnicodeDecodeError:
        return False

if __name__ == '__main__':
    done = False
    print("Test Pickle from Desktop.")
    print("Note: Press the 's' key to send message. Or press 'q' to quit.")
    print("baudrate:",ser.baudrate)
    if ser.baudrate == 9600:
        print(".....Operating in LOOPBACK.....")
        print(".....Operating in LOOPBACK.....")
    cnt = 0
    recv_size = 0
    while not done:
        gc.collect()
        if ser.in_waiting:
            dat = ser.read(1)
            if dat != b'':
                if recv_size == 0:
                    recv_size = int.from_bytes(dat, 'big')
                    print("size", recv_size)
                    buffer = bytearray(recv_size )
                    print("Serial Receiving:")
                else:
                    print(" ",ord(dat),end="")
                    if cnt < recv_size:
                        buffer[cnt] = ord(dat)
                    cnt += 1
                    
                if cnt == (recv_size ):
                    print()
                    ######################################
                    if is_ascii(buffer):
                        recv = buffer.decode()
                        print("Note: buffer is ascii")
                    else:
                        recv = pickle.loads(buffer)
                    ######################################
                    print("Message size:",cnt,"Message:",recv)
                    print("-"*80)
                    recv_size = 0
                    cnt = 0

        if keyboard.is_pressed('q'):
            time.sleep(0.2)
            done = True            

        if keyboard.is_pressed('s'):
            time.sleep(0.2)
            recv_size = 0
            cnt = 0
            ######################################
            message = ( "hello", 15, True, 1.414)
            msg = pickle.dumps(message)
            #msg = msg.encode("utf-8")
            ######################################
            ba = bytearray(1)
            ba[0] = len(msg)
            print("-"*80)
            print("Message size", len(msg),"Message:",message)
            print("Serial Sending:")
            for c in msg:
                print(" ",c,end="")
            print()
            print("-"*80)
            ser.write(ba)
            ser.write(msg)

    ser.close()
    
