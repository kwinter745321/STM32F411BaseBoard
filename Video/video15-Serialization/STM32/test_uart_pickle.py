# test_uart_pickle.py
#
# Copyright (C) 2024 KW Services.
# MIT License
# MicroPython 1.24
#
from machine import Pin, UART
import os
import time

from pickle import pickle
#import array

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

pickle = pickle()
#hold = array.array('l', [1, 2, 3, 4, 5])
### Main Loop ##############
if __name__ == '__main__':

    done = False
    print("Test Pickle on STM32")
    
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
                    recv = pickle.loads(buffer)
                    ######################################
                    print("Message size:",cnt,"Message:",recv)
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
            message = ("hello", 15, True, 1.414)
            #message = {"label":"hello","Var":15}
            #message = {1:'test', 2:1.414, 3: [11, 12, 13]}
            #message = hold   #to send desktop: uncomment import/variable above
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
            uart.write(ba)
            uart.write(msg)
            
        time.sleep_ms(10)

    uart.deinit()
