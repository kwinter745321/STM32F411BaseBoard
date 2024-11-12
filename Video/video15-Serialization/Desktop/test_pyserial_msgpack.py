# test_pyserial_msgpack.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# Python 3.9, pySerial, keyboard
#
import serial
import gc
import time

import msgpack

#pip install keyboard
import keyboard

comport = "COM4"

ser = serial.Serial(port=comport, baudrate=38400, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=False, rtscts=0, dsrdtr=False)
#ser = serial.serial_for_url('loop://', timeout=1)  #desktop

if __name__ == '__main__':
    done = False
    print("Test msgpack from Desktop.")
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
                    recv = msgpack.loads(buffer)
                    if isinstance(recv, msgpack.ext.ExtType):
                        recv2 = msgpack.loads(recv.data)
                        print("Message size:",cnt,"Message2:",recv2)
                    else:
                        print("Message size:",cnt,"Message:",recv)
                    ######################################
                    print("-"*80)
                    recv_size = 0
                    cnt = 0

        if keyboard.is_pressed('q'):
            time.sleep(0.2)
            done = True
        
        if keyboard.is_pressed('s'):
            time.sleep(0.2)
            message = ( "hello", 15, True, 1.414)
            ######################################
            msg = msgpack.dumps(message)
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
    
