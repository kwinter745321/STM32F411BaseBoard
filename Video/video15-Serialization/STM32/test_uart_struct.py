# test_uart_struct.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.24
#
from machine import Pin, UART
import os
import time

import struct

### PIN Definitions ##############
USER_BUTTON_PIN =  const('PB10')
USER2_BUTTON_PIN =  const('PB2')

UART_PORT_NUM = const(1)
UART_SPEED = const(38400)      #use this for the classice Bluetooth device
#UART_SPEED = const(9600)      #use this for DX-BT27-A BT-27 (BLE5.1) device

# UART_TX = const('PA9')
# UART_RX = const('PA10')
#UART_PORT = const('UART1')
### Setup #########################
user = Pin( USER_BUTTON_PIN, Pin.IN, Pin.PULL_UP )
user2 = Pin( USER2_BUTTON_PIN, Pin.IN, Pin.PULL_UP )

uart = UART( UART_PORT_NUM, UART_SPEED )
uart.init( UART_SPEED, bits=8, parity=None, stop=1,timeout=50 )

### Main Loop ##############
if __name__ == '__main__':

    done = False
    print("Test struct on STM32")
    
    print("Starts waiting for data. Press User button to send message.")
    print("Press button-2 or Control-c key to quit.")
    cnt = 0
    recv_size = 0
    while not done:
        user_btn = user.value()
        user2_btn = user2.value()

        if uart.any() > 0:
            dat = uart.read(1)
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
                    fmt = "<5sIif"
                    parts = struct.unpack_from(fmt, buffer, 0)
                    ######################################
                    print("Message size:",cnt,"Message:",parts)
                    print("-"*80)
                    recv_size = 0
                    cnt = 0
                    
        if user2_btn == 0:
            time.sleep_ms(200)
            done = True
            
        if user_btn == 0:
            time.sleep_ms(500)
            recv_size = 0
            cnt = 0
            ######################################
            obj = ( "hello", 15, 1, 1.414)
            fmt = "<5sIif"
            size = struct.calcsize(fmt)
            msg = bytearray(size)
            struct.pack_into(fmt, msg, 0, obj[0],obj[1],obj[2],obj[3])
            ######################################
            print("-"*80)
            i = 0
            for c in msg:
                print(" ",c,end="")
            print()
            ba = bytearray(1)
            ba[0] = size
            print("-"*80)
            print("Message size", size,"Message:",obj)
            print("Serial Sending:")
            for c in msg:
                print(" ",c,end="")
            print()
            print("-"*80)
            uart.write(ba)
            uart.write(msg)
            
        time.sleep_ms(10)

    uart.deinit()
