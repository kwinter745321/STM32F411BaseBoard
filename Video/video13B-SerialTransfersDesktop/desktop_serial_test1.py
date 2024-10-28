# desktop_serial_test1.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# python 3.10
#

import time
from enum import Enum

#pip install pyserial
import serial

# pip install keyboard
import keyboard

### Device Definitions ######################
SERIAL_PORT_SPEED = 38400
SERIAL_PORT = "COM4"

### Constants and Initialize variables ######
START_BYTE = 0x7E #desktop
END_BYTE = 0x7D
ESC_BYTE = 0x7C
BUFFER_SIZE = 16

last_byte = None
payload_size = 0
in_data =  bytearray(BUFFER_SIZE)
in_cnt = 0
hold_checksum = 0
cnt = 0
current_state = 0
### SETUP ###################################
serial = serial.Serial(port=SERIAL_PORT, baudrate=SERIAL_PORT_SPEED)  #desktop
#serial = serial.serial_for_url('loop://', timeout=1)  #desktop

### Functions ###############################
#States for finite state machine
class State(Enum):
    LOCATE_START    = 0
    LOCATE_SIZE     = 1
    LOCATE_PAYLOAD  = 2
    LOCATE_CHECKSUM = 3
    LOCATE_END      = 4
    
def reset():
    global payload_size, last_byte, hold_checksum
    global in_data, in_cnt
    global current_state
    global cnt
    last_byte = None
    payload_size = 0
    in_data =  bytearray(BUFFER_SIZE)
    in_cnt = 0
    hold_checksum = 0
    cnt = 0
    current_state = State.LOCATE_START

# Simple single-byte checksum
def checksum(msg):
    v = 21  
    for c in msg:
        if isinstance(c, str):
            # Convert byte to int
            c = ord(c)
        v ^= c
    return v

# Trim zeros from end of byte array
def trim_zeros(msg):
    loc = len(msg) - 1
    # Check backwards 
    while msg[loc] == 0:
        loc = loc - 1
    newmsg = bytearray(loc)
    newmsg = msg[:loc+1]
    return newmsg

# frame:  START, Size, Message, Checksum, END
def build_frame(msg):
    #----Build frame-----------
    buf = bytearray(BUFFER_SIZE)
    # Insert the START_BYTE
    buf[0] = START_BYTE
    # Insert the size of the message
    size = len(msg)
    buf[1] = size
    # Insert the bytes of the message 
    buf[2:] = msg.encode("utf-8")
    # Insert the checksum
    part = bytearray(1)
    part[0] = checksum(msg)
    buf.extend(part)
    # Insert the END_BYTE
    part[0] = END_BYTE
    buf.extend(part)
    return buf

def byte_stuff(frame):
    cnt = 0
    index = 0
    size = len(frame)
    ready = False
    buf = bytearray(BUFFER_SIZE)
    ba = bytearray(1)
    while not ready:
        if frame[index] in [START_BYTE, END_BYTE, ESC_BYTE] and cnt > 0:
            # Insert an escape byte into the buffer
            buf[cnt] = ESC_BYTE
            cnt = cnt + 1
            # Now place the byte from the frame
            buf[cnt] = frame[index]
            buf.extend(ba)
        else:
            # Otherwise, place the byte from the frame
            buf[cnt] = frame[index]
        if index == size - 1:
            ready = True
        cnt = cnt + 1
        index = index + 1
    return buf  # Return the byte-stuffed frame

def receive(dat):
    global payload_size, last_byte, hold_checksum
    global in_data, in_cnt
    global current_state
    global cnt
    
    if last_byte == None:
        print("  Frame[%d]: dat:%03d  %02x  %c None"% (cnt, dat, dat, dat))
    else:
        print("  Frame[%d]: dat:%03d  %02x  %c %d"% (cnt, dat, dat, dat, last_byte))
    
    # Remove the stuffed ESC byte
    if  dat == ESC_BYTE and last_byte == ESC_BYTE:
        print("esc-esc")
        last_byte = None
      
    if dat == ESC_BYTE and last_byte != None:
        print("esc")
        last_byte = ESC_BYTE
        return None

    # Find CRC
    if current_state == State.LOCATE_CHECKSUM:
        hold_checksum = dat
        current_state = State.LOCATE_END
            
    # Find message
    if current_state == State.LOCATE_PAYLOAD:  
        # ----Found a byte for message
        in_data[in_cnt] = dat
        last_byte = dat
        in_cnt = in_cnt + 1
        # We have all of the bytes for the message
        if in_cnt == payload_size:
            current_state = State.LOCATE_CHECKSUM
            last_byte = None
            
    # Find the payload size
    if current_state == State.LOCATE_SIZE:
        payload_size = dat
        current_state = State.LOCATE_PAYLOAD

    # Find the END byte
    if dat == END_BYTE and last_byte == None:
        #print("END:",dat,last_byte)
        # ----found END byte 
        payload = trim_zeros(in_data)
        calc = checksum(payload)
        #calc = crc16_ccitt(0, payload, len(payload))
        if hold_checksum == calc:
            response = payload
            return payload
        else:
            print(hold_checksum,calc)
            print("\nError on Checksum. Resend message.")
            return None
    
    # Find the START byte
    if dat == START_BYTE and last_byte == None:
        # ----found Start Cbyte
        current_state = State.LOCATE_SIZE
        
    cnt = cnt + 1
    
def send(message):
    frame = build_frame(message )
    frame = byte_stuff(frame)
    frame = trim_zeros(frame)
    cnt = serial.write(frame)
    reset()


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
    #message = msg.encode("utf-8")
    #message = "he" + chr(END_BYTE) + "llo" + chr(ESC_BYTE)
    reset() 
    try:
        while not done:
            
            if serial.in_waiting > 0:
                c = serial.read(1)
            
                dat = ord(c)
                resp = receive(dat)
                if resp != None:
                    print("Received buffer: ",resp)
                    print("-"*85)
                    reset()
                    send("OK")
                
            if keyboard.is_pressed('s'):
                time.sleep(0.5)  #debounce keypress
                print("-"*85)
                print("Pressed s. Will send message:",message)
                
                print("  a) Message:      %s  " % message," "*19,"size:%2d bytes" % len(message))
                frame = build_frame(message )
                print("  b) Frame:        %s  size:%2d bytes" % (frame, len(frame) ) )
                frame = byte_stuff(frame)
                frame = trim_zeros(frame)
                print("  c) Byte-stuffed: %s size:%2d bytes" % (frame, len(frame) ) )
                
                cnt = serial.write(frame)
                print("Sent %d bytes" % cnt)
                reset()
                
                print("-"*85)
                
    except:
        print("Exception or Control-c entered.")
    finally:
        serial.close()
        print("Program finished")