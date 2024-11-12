#!/usr/bin/env python3

# cobs_volts.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# Python 3.9
#

import serial,os,time,serial
from random import randint

'''
File modified from the version at
EEVblog: 
https://www.eevblog.com/forum/microcontrollers/implementing-uart-data-packets-with-consistent-overhead-byte-stuffing-(cobs)/ 
posted by voltsandjolts August 05, 2020
'''

def cobs_encode(message):
    '''
    COBS encoder/stuffer
    Input bytes are encoded such that there are no zero bytes in the output
    '''
    if type(message) != bytes and type(message) != bytearray:
        raise TypeError('Need bytes or bytearray input')
    code = i = 1
    code_idx = 0
    frame = bytearray( 5 + int(len(message)*1.1) )
    for b in message:
        if b == 0:
            frame[code_idx] = code  #FinishBlock
            code = 1
            code_idx = i
            i += 1
        else:
            frame[i] = b
            i += 1
            code += 1
            if code == 0xFF:
                frame[code_idx] = code  #FinishBlock
                code = 1
                code_idx = i
                i += 1
    frame[code_idx] = code  #FinishBlock
    return frame[0:i]

def cobs_decode(frame):
    '''
    COBS decoder/unstuffer
    '''
    if type(frame) != bytes and type(frame) != bytearray:
        raise TypeError('Need bytes or bytearray input')
    msg = bytearray()
    i=0
    while i < len(frame):
        code = frame[i]
        i += 1
        for j in range(1,code):
            if j < len(frame):
                msg.append(frame[i])
            i += 1
        if code < 0xFF:
            msg.append(0)
    return msg[0:-1]


def crc16_ccitt(crc:int, data:bytes) -> int:
    x:int=0
    for i in range(len(data)):
        x = ((crc >> 8) ^ data[i]) & 0xff
        x = x ^ (x >> 4)
        crc = (crc << 8) ^ (x << 12) ^ (x << 5) ^ x
        crc = crc & 0x0ffff
    return crc

def cob_make_frame(msg):
    '''
    msg is the bytearray message we want to send.
    CRC16 is appended, COBS encoded and then zero leading and
    trailing bytes added to complete the frame, ready
    for sending on the wire.
    '''
    if type(msg) != bytes and type(msg) != bytearray:
        raise TypeError('Need bytes or bytearray input')
    m = bytearray(msg)
    crc = crc16_ccitt(0,msg)
    m.extend(bytes([crc >> 8,crc & 0x0FF])) #Append CRC, low byte last. To check later, calculate CRC over all bytes and CRC result should be zero
    enc_msg = cobs_encode(m) #COBS encode
    if 0 in enc_msg:
        raise ArithmeticError #COBS encoded message should not have any zeros in it
    frame = bytearray(len(enc_msg)+2) #Add leading and trailing zero to make frame
    #
    # print("*** COBS encoded Frame  (to be sent):",enc_msg)
    #
    frame[1:-1] = memoryview(enc_msg)
    return frame

def get_frame(serialport, timeout_sec):
    '''
    Build bytearray of uart characters until 0x00 received.
    If timeout occurs any characters received so far are returned.
    '''
    start_time = time.monotonic()
    frame = bytearray()
    while (time.monotonic() - start_time) < timeout_sec:        
        time.sleep(0.010)
        n = serialport.inWaiting()
        for i in range(n):
            c = serialport.read(1)
            if len(c) != 0:
                if c[0] == 0:
                    if len(frame) > 3: #Valid frame must have two byte CRC plus leading COBS code and payload
                        timeout = False
                        return [frame, timeout]
                    else:
                        frame = bytearray() #Found invalid frame (too short), flush and carry on receiving
                else:
                    frame.append(c[0])
    timeout = True
    return [frame, timeout]


def get_msg(serialport, timeout_ms):
    [frame, timeout] = get_frame(serialport, timeout_ms)\
    #
    # if frame != b'':
    #     print("*** COBS encoded Frame (as received):",frame)
    #
    if len(frame) < 4 or timeout:
        return bytearray() #Invalid frame
    msg = cobs_decode(frame)
    crc = crc16_ccitt(0,msg)    
    if len(msg) < 3 or crc != 0:
        return bytearray() #Invalid message
    return msg[0:-2]

def send_msg(serialport, msg):
    frame=cob_make_frame(msg)
    serialport.write(frame)

#-----------------   Allow execution as a program or as a module  -----------------------
if __name__ == '__main__':
    print("COBS Loopback Test")
    #uart = serial.Serial(port=comport, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=False, rtscts=0, dsrdtr=False)
    uart = serial.serial_for_url('loop://', timeout=1)  #desktop
    total=0
    bad=0
    for i in range(100):
        #msgtx = bytearray.fromhex('0102030405060708090A0B0C0D0E0F') #Or put any sequence of bytes you want to send here
        msgtx = os.urandom(randint(1,200)) # Random bytes for loopback test
        send_msg(uart, msgtx)
        msgrx = get_msg(uart, 1)
        if msgrx != msgtx:
            bad += 1
        total += 1
        print("Good:\t",total-bad,"\tBad:\t",bad)
    uart.close()


#export
__all__ = ["send_msg", "get_msg"]
