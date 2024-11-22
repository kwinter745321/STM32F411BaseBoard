# stm32_uart_test1.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.20 
#
from machine import Pin, UART
import time
from enum import Enum
import struct
### PIN Definitions ##############
USER_BUTTON_PIN =  const('PB10')

UART_PORT_NUM = const(1)
UART_SPEED = const(38400)      #use this for the classice Bluetooth device
#UART_SPEED = const(9600)      #use this for DX-BT27-A BT-27 (BLE5.1) device

# UART_TX = const('PA9')
# UART_RX = const('PA10')
#UART_PORT = const('UART1')
### Setup #########################
user = Pin( USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP )
uart = UART( UART_PORT_NUM, UART_SPEED )
uart.init( UART_SPEED, bits=8, parity=None, stop=1,timeout=50 )

#States for finite state machine
class State(Enum):
    LOCATE_START    = 0
    LOCATE_ID       = 1
    LOCATE_OVHD     = 2
    LOCATE_SIZE     = 3
    LOCATE_PAYLOAD  = 4
    LOCATE_CHECKSUM = 5
    LOCATE_END      = 6

### Constants and Initialize variables ##############
# START_BYTE = const(0x7C)
# END_BYTE = const(0x7E)
# ESC_BYTE = const(0x7D)
START_BYTE = const(0x7E)
END_BYTE = const(0x81)

MAX_PACKET_SIZE = 0xFE

last_byte = None
payload_size = 0
in_data =  bytearray(MAX_PACKET_SIZE)
in_cnt = 0
rec_ohb = 0 # received overhead byte
hold_checksum = 0
cnt = 0
current_state = State.LOCATE_START

### Functions #####################

    
def reset():
    global payload_size, last_byte, hold_checksum
    global MAX_PACKET_SIZE
    global packet_id, in_data, in_cnt
    global rec_ohb
    global cnt
    global current_state
    
    payload_size = 0
    last_byte = None
    hold_checksum = 0
    
    packet_id = 0
    in_data =  bytearray(MAX_PACKET_SIZE)
    in_cnt = 0
    
    rec_ohb = 0
    cnt = 0
    current_state = State.LOCATE_START

# Simple single-byte checksum
def checksum(msg):
    crc = calculate(msg,len(msg))
    return crc

def calculate_checksum(index: int):
    """Calculate the checksum for a given index.
    An LRU cached version of the CRC calculation function,
    with an upper bound on the cache size of 2^16
    """
    polynomial = 0x9B
    poly = polynomial & 0xFF
    crc_len=8
    table_len = pow(2, crc_len)
    if index > table_len:
        raise ValueError('Index out of range')
    curr = index
    for j in range(8):
        if (curr & 0x80) != 0:
            curr = ((curr << 1) & 0xFF) ^ poly
        else:
            curr <<= 1
    return curr

def calculate(arr, dist=None):
    crc = 0
    try:
        if dist:
            indicies = dist
        else:
            indicies = len(arr)
        for i in range(indicies):
            try:
                nex_el = int(arr[i])
            except ValueError:
                nex_el = ord(arr[i])
            crc = calculate_checksum(crc ^ nex_el)
    except TypeError:
        crc = calculate_checksum(arr)
    return crc

# # Trim zeros from end of byte array
# def trim_zeros(msg):
#     #print("trim",len(msg),msg)
#     if msg[0] == 0:
#         return None
#     loc = len(msg) - 1
#     # Check backwards 
#     while msg[loc] == 0:
#         loc = loc - 1
#     newmsg = bytearray(loc)
#     newmsg = msg[:loc+1]
#     return newmsg

def calc_overhead(msg, pay_len):
    overhead_byte = 0xFF
    print("calc-ovhd",pay_len,msg)
    for i in range(pay_len):
        if msg[i] == START_BYTE:
            overhead_byte = i
            break
    return overhead_byte

# frame:  START, Size, Message, Checksum, END
def build_frame(msg):
    #----Build frame-----------
    buf = bytearray(MAX_PACKET_SIZE)
    # Insert the START_BYTE
    buf[0] = START_BYTE
    buf[1] = 0x00 #  packet_id
    # size of msg
    pay_len = len(msg)
    ohb = calc_overhead(msg, pay_len)
    buf[2] = ohb
    # Insert the size of the message
    buf[3] = pay_len
    # Insert the bytes of the message
    
    print("  b) Msg:        %s  size:%2d bytes" % (msg, len(msg) ) )
    msg = byte_stuff(msg)
    print("  c) Byte-stuffed: %s size:%2d bytes" % (msg, len(msg) ) )
    
    buf[4:] = msg   #.encode("utf-8")
    # Insert the checksum
    part = bytearray(1)
    crc = checksum(msg)
    part[0] = crc
    buf.extend(part)
    # Insert the END_BYTE
    ba = bytearray(1)
    ba[0] = END_BYTE
    buf.extend(ba)
    return buf

def find_last(frame, pay_len):

    if pay_len <= MAX_PACKET_SIZE:
        for i in range(pay_len - 1, -1, -1):
            if frame[i] == START_BYTE:
                return i
    return -1

def byte_stuff(frame):
    pay_len = len(frame)
    ref_byte = find_last(frame, pay_len)

    if (not ref_byte == -1) and (ref_byte <= MAX_PACKET_SIZE):
        for i in range(pay_len - 1, -1, -1):
            #print(" %02x" % frame[i], end="")
            if frame[i] == START_BYTE:
                #print("## %02x %02x %02x  ##" % (frame[i],i,ref_byte), end="")
                frame[i] = ref_byte - i
                ref_byte = i

    return frame

def byte_unstuff(buf, rec_ohb):  
    test_index = rec_ohb   # rec_overhead_byte
    print("unstuff  received OHB:",rec_ohb)
    
    if test_index <= MAX_PACKET_SIZE:
        while buf[test_index]:
            delta = buf[test_index]
            buf[test_index] = START_BYTE
            test_index += delta
        buf[test_index] = START_BYTE
    return buf

def receive(dat):
    global payload_size, last_byte, hold_checksum
    global in_data, in_cnt
    global current_state
    global cnt
    global rec_ohb
    
    if last_byte == None:
        if dat == 0:
            print("  Frame[%d]: dat:000  00  0 None state:%d"% (cnt, current_state))
        else:
            print("  Frame[%d]: dat:%03d  %02x  %c None state:%d"% (cnt, dat, dat, dat, current_state))
    else:
        print("  Frame[%d]: dat:%03d  %02x  %c %04d state:%d"% (cnt, dat, dat, dat, last_byte, current_state))
    
#     # Remove the stuffed ESC byte
#     if  dat == ESC_BYTE and last_byte == ESC_BYTE:
#         print("esc-esc")
#         last_byte = None
#       
#     if dat == ESC_BYTE and last_byte != None:
#         print("esc")
#         last_byte = ESC_BYTE
#         return None

    # Find CRC
    if current_state == State.LOCATE_CHECKSUM:
        hold_checksum = dat
        print("crc:",hold_checksum)
        current_state = State.LOCATE_END
        last_byte = None
            
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
        
    # Find the payload size
    if current_state == State.LOCATE_OVHD:
        rec_ohb = dat
        current_state = State.LOCATE_SIZE
            
    # Find the payload size
    if current_state == State.LOCATE_ID:
        packet_id = dat
        current_state = State.LOCATE_OVHD

    # Find the END byte
    if current_state == State.LOCATE_END and dat == END_BYTE:
        print("END:",dat,last_byte)
        # ----found END byte
        #payload = trim_zeros(in_data)
        payload = in_data[:payload_size]
        calc_crc = checksum(payload)
        print(payload)
        payload = byte_unstuff(in_data[:payload_size], rec_ohb)
        print("Unstuffed payload:",payload[:payload_size])
        
        if payload == None:
            return None
        #found_crc = checksum(payload)
        #print("Checksum  rec, calc:", hold_checksum, calc_crc)
        if hold_checksum == calc_crc:
            response = payload
            return payload
        else:
            #print(hold_checksum,calc_crc)
            print("\nError on Checksum. Resend message.")
            return None
    
    # Find the START byte
    if dat == START_BYTE and last_byte == None:
        # ----found Start Cbyte
        current_state = State.LOCATE_ID
        

        
    cnt = cnt + 1
    

### Loop ##########################
done = False
reset()  
print("----------------")
print("Program started (to send message via UART ).")

prompt = "Press User button to send data or Control-c in Shell to exit."
print(prompt)
print("-"*85)
print(" Frame: [Start] [Size] [Payload1][Payload2]...[Payloadn] [Checksum byte] [End]")
print("-"*85)
while not done:
    user_btn = user.value()
    
    if uart.any() > 0:
        if cnt == 0:
            print("Receiving data...")
        c = uart.read(1)
        
        dat = ord(c)
        resp = receive(dat)
        if resp != None:
            print("Received buffer: ",resp)
            print("-"*85)
            ######################################
            fmt = "<Iif5s"
            parts = struct.unpack_from(fmt, resp, 0)
            ######################################
            print("Message size:",cnt,"Message:",parts)
            reset()

    if user_btn == 0:
        time.sleep(0.5)
        print("Sending data...")
        ##################################################################
        fmt = "<Iif5s"
        msg_len = struct.calcsize(fmt)
        message = bytearray(msg_len)
        offset = 0
        hello = bytearray(5)
        i = 0
        for c in "hel~o":
            hello[i] = ord(c)
            i=i+1
        #hello[3] = START_BYTE
        struct.pack_into(fmt, message, offset, 15,1,1.414,hello)
        ##################################################################
        print("  a) Message:      %s  " % message," "*19,"size:%2d bytes" % len(message))
        frame = build_frame(message )
        if frame[0] == 0:
            break
        #frame = trim_zeros(frame)
        if frame == None:
            print("frame is None")
            done = True
            break
        
        
        #-------------------------
        cnt = uart.write(frame)
        print("  d) Transmitted:  %s size:%2d bytes" % (frame, cnt) )
        reset()
        print("-"*85)
            
# except KeyboardInterrupt:
#     done = True
#     print('Interrupted by Control-c.')
# finally:
uart.deinit()
print('Finished.')